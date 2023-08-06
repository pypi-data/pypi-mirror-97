import asyncio
import logging
import pprint
import sys
import threading
import time
import warnings
from contextlib import contextmanager, asynccontextmanager
from random import random
from typing import Dict, Tuple, List, Iterator, Generator, AsyncGenerator

from sqlalchemy import event, ForeignKeyConstraint
from sqlalchemy.orm import sessionmaker, Session

from constellate.database.sqlalchemy.exception.vacumexception import VacumException
from constellate.database.sqlalchemy.multienginesession import MultiEngineSession
from constellate.database.sqlalchemy.relationshiptype import RelationshipType
from constellate.database.sqlalchemy.sessiontype import SessionType
from constellate.database.sqlalchemy.sqlalchemydbconfig import DBConfigType, SQLAlchemyDBConfig


def _warn_no_per_engine_option_found(options: Dict):
    engines = options.get("engines", None)
    if engines is None:
        warnings.warn(
            "options must be configured per engine. {engines:[{your options here}]}",
            DeprecationWarning,
        )


def _extract_engine_ids(options: Dict):
    engines = options.get("engines", [])
    engines_ids = [e.get("id", None) for e in engines]
    if None in engines_ids:
        raise ValueError("1+ engine is missing field: id")
    return engines_ids


def _get_engine_options(options: Dict) -> List[Dict]:
    _warn_no_per_engine_option_found(options)

    engines = options.get("engines", [])
    if len(engines) == 0:
        engines = [{"id": "default", **options}]
    return engines


def session_scope(session_maker: sessionmaker = None, **kwargs) -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    session = session_maker(**kwargs)
    try:
        yield session
        session.commit()
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()


async def async_session_scope(
    session_maker: sessionmaker = None, **kwargs
) -> AsyncGenerator[Session, None]:
    """Provide a transactional scope around a series of operations."""
    # FIXME NOT FUNCTIONAL YET
    session = session_maker(**kwargs)
    try:
        yield session
        session.commit()
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()


class SQLAlchemy:
    """
    Use SQLAlchemy to interact with db
    Typical usage:
        s = SQLAlchemy()
        s.setup(...)
        s.reflect_schema(...)
    """

    def __int__(self):
        self._session_type = SessionType.UNKNOWN
        self._instances = {}

    def _engines(
        self, engine_options: List[Dict], types: List[DBConfigType] = [DBConfigType.INSTANCE]
    ) -> Iterator[Tuple[SQLAlchemyDBConfig, Dict]]:
        engine_id_to_options = {
            engine_options.get("id"): engine_options for engine_options in engine_options
        }
        instance_id_to_instances = {k: v for k, v in self._instances.items() if v.type in types}

        mapping = []
        for identifier, instance in instance_id_to_instances.items():
            e_options = engine_id_to_options.get(identifier, None)
            if e_options is not None:
                mapping.append((instance, e_options))

        return iter(mapping)

    @contextmanager
    def setup(self, options: Dict = {}):
        """
        :options: See each _setup_engine_XXXX method for available options in addition to the options below
        - key: engines: Per engine options
        -- Key: type: "instance" (default) => SQLAlchemy will connect to it. "template" SQLAlchemy will use the config for later
        -- Key: id:str. Any string value except "default"
        -- Key: logger:logging.Logger. Default: None

        Eg:
        options = {
            "engines": [
                {
                    "type": "instance",
                    "id": "shard_main",
                    "logger": ...
                },
                {
                    "type": "template",
                    "id": "shard_slave",
                    "logger": ...
                }
            ]
        }
        """
        setup_engines_options = []
        try:
            for engine_options in _get_engine_options(options):
                db_config_type = (
                    DBConfigType.INSTANCE
                    if engine_options.get("type", "instance") == "instance"
                    else DBConfigType.TEMPLATE
                )

                if self._session_type == SessionType.UNKNOWN:
                    self._session_type = SessionType.MONO_ENGINE
                elif self._session_type == SessionType.MONO_ENGINE:
                    self._session_type = SessionType.MULTI_ENGINE

                instance = SQLAlchemyDBConfig()
                instance.identifier = engine_options.get("id", None)
                instance.type = db_config_type
                instance.options = engine_options
                instance.logger = engine_options.get("logger", None)
                instance.logger.debug(f"setup database context: started")
                self._setup(instance=instance, options=engine_options)
                instance.logger.debug(f"setup database context: completed")
                self._instances.update({instance.identifier: instance})
                setup_engines_options.append(engine_options)

            yield self
        finally:
            for engine_options in setup_engines_options:
                self.dispose(engine_options)

    def _setup(self, instance: SQLAlchemyDBConfig = None, options: Dict = {}):
        instance.connection_uri, instance.engine = self._create_engine(options=options)
        self._setup_engine_logging(instance=instance, engine=instance.engine, options=options)
        self._setup_engine_before_cursor_execute(
            instance=instance, engine=instance.engine, options=options
        )
        self._setup_engine_after_cursor_execute(
            instance=instance, engine=instance.engine, options=options
        )
        self._setup_engine_connection_connect(
            instance=instance, engine=instance.engine, options=options
        )
        self._setup_engine_connection_begin(
            instance=instance, engine=instance.engine, options=options
        )
        self._setup_engine_session_maker(instance=instance)

    def _create_engine(self, options: Dict = {}) -> Tuple[str, object]:
        raise NotImplementedError("Subclass must implemented")

    def _setup_engine_logging(
        self, instance: SQLAlchemyDBConfig, engine: object = None, options: Dict = None
    ):
        if options.get("is_production", False):
            severity1 = logging.INFO if options.developer else logging.WARN
            severity2 = logging.DEBUG if options.developer else logging.INFO
            # Turn on SQL Query logging
            logging.getLogger("sqlalchemy").setLevel(severity1)
            logging.getLogger("sqlalchemy.engine").setLevel(severity1)
            logging.getLogger("sqlalchemy.dialects").setLevel(severity1)
            # Turn on Connection Pool usage logging
            logging.getLogger("sqlalchemy.pool").setLevel(severity2)
            # Turn on other things
            logging.getLogger("sqlalchemy.orm").setLevel(severity2)
            instance.logger.setLevel(logging.DEBUG)
        else:
            instance.logger.setLevel(logging.WARN)

    def _setup_engine_before_cursor_execute(
        self, instance: SQLAlchemyDBConfig, engine=None, options: Dict = None
    ):
        # Profile SQL query execution time
        @event.listens_for(engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            context._query_start_time = time.time()
            instance.logger.debug("Start Query:\n%s" % statement)
            # Modification for StackOverflow answer:
            # Show parameters, which might be too verbose, depending on usage..
            instance.logger.debug("Parameters:\n%r" % (parameters,))

    def _setup_engine_after_cursor_execute(
        self, instance: SQLAlchemyDBConfig, engine=None, options: Dict = None
    ):
        @event.listens_for(engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            total = time.time() - context._query_start_time
            instance.logger.debug("Query Complete!")
            # Modification for StackOverflow: times in milliseconds
            instance.logger.debug("Total Time: %.02fms" % (total * 1000))

    def _setup_engine_connection_connect(
        self, instance: SQLAlchemyDBConfig, engine=None, options: Dict = None
    ):
        pass

    def _setup_engine_connection_begin(
        self, instance: SQLAlchemyDBConfig, engine=None, options: Dict = None
    ):
        pass

    def reflect_schema(
        self,
        options: Dict = {},
        entity_base_class: object = None,
        entity_classes: List[object] = [],
        scalar_relation_mapping: List[Tuple] = [],
        collection_direct_relation_mapping: List[Tuple] = [],
        collection_indirect_relation_mapping: List[Tuple] = [],
    ):
        for instance, i_options in self._engines(_get_engine_options(options)):
            try:
                instance.logger.info(f"Reflect db schema: started")
                self._reflect_schema(
                    instance=instance,
                    entity_base_class=entity_base_class,
                    entity_classes=entity_classes,
                    scalar_relation_mapping=scalar_relation_mapping,
                    collection_direct_relation_mapping=collection_direct_relation_mapping,
                    collection_indirect_relation_mapping=collection_indirect_relation_mapping,
                )
                instance.logger.info(f"Reflect db schema: completed")
            except BaseException:
                instance.logger.error(f"Reflect db schema: failed", exc_info=1)
                raise

    def _reflect_schema(
        self,
        instance: SQLAlchemyDBConfig = None,
        entity_base_class: object = None,
        entity_classes: List[object] = [],
        scalar_relation_mapping: List[Tuple] = [],
        collection_direct_relation_mapping: List[Tuple] = [],
        collection_indirect_relation_mapping: List[Tuple] = [],
    ):
        """
        Reflect tables + relations
        :entity_base_class: See example

        from sqlalchemy.ext.automap import automap_base
        Base = automap_base()

        Base *is* the entity_base_class

        :scalar_relation_mapping, collection_direct_relation_mapping, collection_indirect_relation_mapping: See example
        class Table(Enum):
            FAVORITE = "favorites"
            FOLLOWER_NAMES = "followers_names"
            FOLLOWER = "followers"
            FOLLOWING = "following"
            FOLLOWING_NAMES = "following_names"
            QUOTEAGG = "view_quotes_aggregate"
            REPLY = "replies"
            RETWEET = "retweets"
            QUOTE = "quotes"
            TWEET = "tweets"
            USER = "users"

        scalar_relation_mapping = [
            "FromEntity name", "entity property name", "ToEntity name", "entity property name", "relation name (stored in FromEntity)"
            (Table.FAVORITE.value, "user_id", Table.USER.value, "id", "user") ==> "Favorite.user is the scalar relation Favorite.user_id->User.id"
            (Table.FAVORITE.value, "tweet_id", Table.TWEET.value, "id", "tweet")
        ]

        collection_indirect_relation_mapping = [
           ("FromEntity name", "entity property name", "ToFinalEntity nane", "entity property name", "ViaEntityStart name", "entity property name", "ViaEntityEnd", "entity property name", "Relation Name", "Reverse Relation Name")
           ( Table.TWEET.value, "id", Table.USER.value, "id", Table.FAVORITE.value, "tweet_id", Table.FAVORITE.value, "user_id", "favorited_by", "favorited")
                ==> Tweet.favorited_by is the collection relation Tweet.id->Favorite.tweet_id->Favorite.user_id->User.id
                ==> User.favorited is the collection relation User.id->Favorite.user_id->Favorite.tweet_id->Tweet.id
        ]

        collection_direct_relation_mapping = [
           ("FromEntity name", "entity property name", "ToFinalEntity nane", "entity property name", "Relation Name", "Reverse Relation Name")
           ( Table.TWEET.value, "id", Table.USER.value, "id", "froms", "tweets")
                ==> Tweet.froms is the collection relation Tweet.id->User.id
                ==> User.tweets is the collection relation User.id->Tweet.id
        ]


        """

        def name_for_collection_relationship(base, local_cls, referred_cls, constraint):
            relation_src_table_id = local_cls.__table__.name
            relation_dst_table_id = referred_cls.__table__.name

            reflexive_relation = relation_src_table_id == relation_dst_table_id

            assert len(constraint.column_keys) < 2
            assert len(constraint.elements) < 2

            third_party_tables = list(
                filter(
                    lambda table: table.name not in [relation_src_table_id, relation_dst_table_id],
                    [constraint.table, constraint.referred_table],
                )
            )
            indirect_relation = len(third_party_tables) > 0

            if indirect_relation:
                intermediary_tables = third_party_tables
            else:
                intermediary_tables = [constraint.table]

            def to_relation_string(
                src_table_id,
                src_columns_id,
                dst_table_id,
                dst_columns_id,
                intermediary_relation_path=None,
            ):
                intermediary_relation_path = (
                    f"=>{intermediary_relation_path}=>"
                    if intermediary_relation_path is not None
                    else "=>"
                )
                return f"{src_table_id}.{src_columns_id}{intermediary_relation_path}{dst_table_id}.{dst_columns_id}"

            def via_relation_path(
                src_table_id, src_columns_id, dst_table_id, dst_columns_id, backref
            ):
                if None not in [src_table_id, src_columns_id, dst_table_id, dst_columns_id]:
                    if not backref:
                        return f"{src_table_id}.{src_columns_id}~~~{dst_table_id}.{dst_columns_id}"
                    else:
                        return f"{dst_table_id}.{dst_columns_id}~~~{src_table_id}.{src_columns_id}"
                return None

            # Find transitive relation (ie intermediary table)
            inter_table = intermediary_tables[0]
            inter_fkcs = [
                fk for fk in inter_table.constraints if isinstance(fk, ForeignKeyConstraint)
            ]

            # Find foreign keys constraints of the intermediary table, matching our relation start/end table
            # - These keys will *individually* point to either the relation's source table or the relation's destination table
            relation_to_src__inter_fkc = None
            relation_to_dst__inter_fkc = None

            for inter_fkc in inter_fkcs:
                inter_fk_dst_table_id = inter_fkc.referred_table.name
                if (
                    inter_fk_dst_table_id == relation_src_table_id
                    and relation_to_src__inter_fkc is None
                ):
                    relation_to_src__inter_fkc = inter_fkc
                elif inter_fk_dst_table_id == relation_dst_table_id:
                    relation_to_dst__inter_fkc = inter_fkc

            # Sanity check:
            #  - Indirect relations must have both variable set
            #  - Direct relations only one. By default it will be relation_to_src__inter_fkc
            if (
                indirect_relation
                and not reflexive_relation
                and None in [relation_to_src__inter_fkc, relation_to_dst__inter_fkc]
            ):
                raise BaseException("What's going on here ???")
            if indirect_relation and reflexive_relation:
                pass
                # else:
                #     relation_to_src__inter_fkc = relation_to_dst__inter_fkc if relation_to_dst__inter_fkc is not None else relation_to_src__inter_fkc
                #     relation_to_dst__inter_fkc = relation_to_src__inter_fkc if relation_to_src__inter_fkc is not None else relation_to_dst__inter_fkc
            if not indirect_relation:
                relation_to_src__inter_fkc = (
                    relation_to_dst__inter_fkc
                    if relation_to_dst__inter_fkc is not None
                    else relation_to_src__inter_fkc
                )
                relation_to_dst__inter_fkc = None

            # Find the starting/ending tables associated to the foreign key constraint
            inter_fk_src_table_id = None
            inter_fk_dst_table_id = None
            inter_fk_src_referred_table_id = None
            # inter_fk_dst_referred_table_id = None
            if indirect_relation:
                inter_fk_src_table_id = relation_to_src__inter_fkc.table.name
                inter_fk_dst_table_id = relation_to_dst__inter_fkc.table.name
                inter_fk_src_referred_table_id = relation_to_src__inter_fkc.referred_table.name
                # inter_fk_dst_referred_table_id = relation_to_dst__inter_fkc.referred_table.name
            else:
                inter_fk_src_table_id = relation_to_src__inter_fkc.table.name
                inter_fk_dst_table_id = relation_to_src__inter_fkc.referred_table.name
                inter_fk_src_referred_table_id = None
                # inter_fk_dst_referred_table_id = None

            # Find the column of each matching foreign key used as either starting
            # point or ending point of the relation's table
            relation_src_columns_id = None
            relation_dst_columns_id = None
            if indirect_relation:
                relation_src_columns_id = relation_to_src__inter_fkc.elements[0].column.key
                relation_dst_columns_id = relation_to_dst__inter_fkc.elements[0].column.key
            else:
                relation_src_columns_id = relation_to_src__inter_fkc.elements[0].column.key
                relation_dst_columns_id = relation_to_src__inter_fkc.columns[
                    relation_to_src__inter_fkc.column_keys[0]
                ].key

            inter_fk_end0_columns_id = None
            inter_fk_end1_columns_id = None
            if indirect_relation:
                inter_fk_end0_columns_id = ",".join(
                    [
                        relation_to_src__inter_fkc.columns[col_key].key
                        for col_key in relation_to_src__inter_fkc.column_keys
                    ]
                )
                inter_fk_end1_columns_id = ",".join(
                    [
                        relation_to_dst__inter_fkc.columns[col_key].key
                        for col_key in relation_to_dst__inter_fkc.column_keys
                    ]
                )
            else:
                inter_fk_end0_columns_id = None
                inter_fk_end1_columns_id = None

            # Determine if relation is a backref
            backref = None
            if indirect_relation and relation_src_table_id != relation_dst_table_id:
                # Case: A to C via B (ie non reflexive + indirect relation)
                backref = relation_src_table_id > relation_dst_table_id
            elif indirect_relation and relation_src_table_id == relation_dst_table_id:
                # Case: A to A via B  (ie reflexive + indirect reflexion)
                backref = relation_to_src__inter_fkc.name > relation_to_dst__inter_fkc.name
            else:
                # Case: A to B (ie direct relation)
                backref = relation_src_table_id != inter_fk_src_table_id

            def relation(
                src_table_id, src_columns_id, dst_table_id, dst_columns_id, backref, via_path
            ):
                if backref:
                    resolution_path = to_relation_string(
                        dst_table_id, dst_columns_id, src_table_id, src_columns_id, via_path
                    )
                else:
                    resolution_path = to_relation_string(
                        src_table_id, src_columns_id, dst_table_id, dst_columns_id, via_path
                    )
                return resolution_path

            # Swap intermediary columns if the relation is a backref and the
            # intermediary foreign key to source association is backward
            inter_src_table_id = inter_fk_src_table_id
            inter_dst_table_id = inter_fk_dst_table_id
            inter_end0_columns_id = None
            inter_end1_columns_id = None
            backref_inter = backref and relation_src_table_id == inter_fk_src_referred_table_id
            if backref_inter:
                inter_end0_columns_id = inter_fk_end0_columns_id
                inter_end1_columns_id = inter_fk_end1_columns_id
            else:
                inter_end0_columns_id = inter_fk_end1_columns_id
                inter_end1_columns_id = inter_fk_end0_columns_id
            indirect_path = via_relation_path(
                inter_src_table_id,
                inter_end0_columns_id,
                inter_dst_table_id,
                inter_end1_columns_id,
                not backref,
            )

            relation_path = None
            if backref:
                relation_path = relation(
                    relation_dst_table_id,
                    relation_dst_columns_id,
                    relation_src_table_id,
                    relation_src_columns_id,
                    True,
                    indirect_path,
                )
            else:
                relation_path = relation(
                    relation_src_table_id,
                    relation_src_columns_id,
                    relation_dst_table_id,
                    relation_dst_columns_id,
                    False,
                    indirect_path,
                )

            def via_relation_path_builder(
                src_table_id, src_column_id, dst_table_id, dst_column_id, backref
            ):
                if backref:
                    return via_relation_path(
                        dst_table_id, dst_column_id, src_table_id, src_column_id, False
                    )
                return via_relation_path(
                    src_table_id, src_column_id, dst_table_id, dst_column_id, False
                )

            # Mapping such as Table.A.col_a -> Table.B.col_b MUST ALWAYS BE expressed in the same direction as in the
            # SQL schema's defined relations. More on the relation's "order" below.
            VIA_NONE = via_relation_path(None, None, None, None, backref)
            mapping_indirects = {
                #
                # Indirect relations:
                # relation(A, col_a, B, col_b, ..., via_relation_path(C, col_c0, C, col_c1))
                #  - A < B must be lexicographically ordered true. relation definition MUST be in lexicographic order.
                #  -- relation(A, .., B, ...) is well defined
                #  -- relation(B, .., A, ...) is not well defined
                #  - A > B means the relation is a backref. This is an arbitrary decision when dealing with indirect
                #                                            relations
                #  - reads as the relation is resolved from A.col_a -> C.col_c0 ~~~~ C.col_c1 -> B.col_b
                # relation(Table.USER.value, 'following_id', Table.USER.value, 'id', backref, NO_INTER_RELATION):
                # 'booz6' if not backref else 'zoob6',
                # relation(Table.USER.value, 'following_id', Table.USER.value, 'id', backref, NO_INTER_RELATION):
                # 'booz5' if not backref else 'zoob5',
                # relation(Table.USER.value, 'id', Table.USER.value, 'id', backref, NO_INTER_RELATION):
                # 'booz4' if not backref else 'zoob4',
                # relation(Table.USER.value, 'follower_id', Table.USER.value, 'id', backref, NO_INTER_RELATION):
                # 'booz3' if not backref else 'zoob3',
                # relation(Table.USER.value, 'tweet_id', Table.TWEET.value, 'id', backref, NO_INTER_RELATION):
                # 'booz' if not backref else 'favorited_by_users',
                relation(
                    t[0],
                    t[1],
                    t[2],
                    t[3],
                    backref,
                    via_relation_path_builder(t[4], t[5], t[6], t[7], backref),
                ): t[8]
                if not backref
                else t[9]
                for t in collection_indirect_relation_mapping
            }

            mapping_directs = {
                #
                # Direct relations
                # relation(A, col_a, B, col_b, ...) ==> reads as the relation
                #  - A < B must be in the same order as the foreign key constraint defined in the table betweet A and B for the columns
                #  -- A > B means the relation is a backref as defined by SQLAlchemy
                #  - reads as resolved from A.col_a -> B.col_b
                # resolution(Table.TWEET.value, 'user_id', Table.USER.value, 'id', backref, NO_INTER_RELATION):
                # 'booz2' if not backref else 'favorited_tweets',
                relation(t[0], [1], t[2], t[3], backref, VIA_NONE): t[4] if not backref else t[5]
                for t in collection_direct_relation_mapping
            }

            mapping = {**mapping_indirects, **mapping_directs}

            name = mapping.get(relation_path, None)

            via_relation = "N/A" if not indirect_relation else indirect_path
            relationship_type = None
            if not backref:
                if indirect_relation:
                    relationship_type = RelationshipType.MANY_TO_MANY
                else:
                    relationship_type = RelationshipType.MANY_TO_ONE
            else:
                if indirect_relation:
                    relationship_type = RelationshipType.MANY_TO_MANY
                else:
                    relationship_type = RelationshipType.ONE_TO_MANY

            name = f"RANDOMLY_ASSIGNED-{random()}" if name is None else name

            instance.logger.debug(
                f"---\ncollection relationship name: \nBACKREF:{backref}\nFROM({'backref' if backref else ''}): {relation_src_table_id} \nTO({'backref' if backref else ''}):{relation_dst_table_id}\nINDIRECT RELATION:{indirect_relation}\nVIA:{via_relation}\nVIA(RAW):{str(constraint)}\nBECOMES: {relationship_type} {relation_src_table_id}.{name}\nDUE TO RELATION PATH:{relation_path} \nON MAPPING:\n{pprint.PrettyPrinter(depth=4).pformat(mapping)})"
            )

            if name is None:
                raise BaseException(
                    f"key {relation_path} has no matching relationship name. Missing a case ?"
                )

            return name

        def name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
            relation_src_table_id = local_cls.__table__.name
            relation_dst_table_id = referred_cls.__table__.name

            def relation(src_table_id, src_columns_name, dst_table_id, dst_columns_name):
                return f"{src_table_id}.{src_columns_name}->{dst_table_id}.{dst_columns_name}"

            constraint_src_table_columns_name = ",".join(
                [constraint.columns[col_key].key for col_key in constraint.column_keys]
            )
            constraint_dst_table_columns_name = ",".join(
                [foreign_key.column.key for foreign_key in constraint.elements]
            )

            relation_path = relation(
                relation_src_table_id,
                constraint_src_table_columns_name,
                relation_dst_table_id,
                constraint_dst_table_columns_name,
            )
            relationship_type = RelationshipType.ONE_TO_ONE

            # Mapping always expressed in the same direction as in the sql schema
            mapping = {relation(t[0], t[1], t[2], t[3]): t[4] for t in scalar_relation_mapping}
            name = mapping.get(relation_path, None)

            if name is None:
                raise BaseException(
                    f"key {relation_path} has no matching relationship name. Missing a case ?"
                )

            instance.logger.debug(
                f"scalar relationship name:\nFROM:{relation_src_table_id}\nTO:{relation_dst_table_id}\nBY {str(constraint)}\nBECOMES:{relationship_type} {relation_src_table_id}.{name}\nDUE TO RESOLUTION PATH:{relation_path}"
            )
            return name

        entity_base_class.prepare(
            instance.engine,
            reflect=True,
            name_for_collection_relationship=name_for_collection_relationship,
            name_for_scalar_relationship=name_for_scalar_relationship,
        )

        # Force checking db classes & relationships are automapped and/or manually mapped
        instance.logger.debug("Table(s) relationships:")
        from sqlalchemy.inspection import inspect

        for entity_cls in entity_classes:
            relations = inspect(entity_cls).relationships.items()
            for relation in relations:
                instance.logger.debug(
                    f"Table {entity_cls.__name__} has relationship: -> {relation}"
                )

    def migrate(self, options: Dict = {}):
        """
        :options per engine:
        - key: migration_dirs:List[PurePath], list of absolute path to sql migration scripts
        """
        for instance, i_options in self._engines(_get_engine_options(options)):
            try:
                instance.logger.info(f"Migrating db schema: started")
                self._migrate(instance=instance, options=i_options)
                instance.logger.info(f"Migrating db schema: completed")
            except BaseException:
                instance.logger.error(f"Migrating db schema: failed", exc_info=1)
                raise

    def _migrate(self, instance: SQLAlchemyDBConfig = None, options: Dict = {}):
        raise NotImplementedError("Must be implemented by the sub class")

    def vacuum(self, options: Dict = {}):
        """
        :raises:
            VacumException when vacum fails
        """
        for instance, i_options in self._engines(_get_engine_options(options)):
            try:
                instance.logger.info(f"Vacumming db: started")
                self._vacuum(instance=instance, options=i_options)
                instance.logger.info(f"Vacumming db: completed")
            except BaseException as e:
                instance.logger.error(f"Vacumming db: failed", exc_info=1)
                raise VacumException() from e

    def _vacuum(self, instance: SQLAlchemyDBConfig = None, options: Dict = {}):
        raise NotImplementedError("Must be implemented by the sub class")

    def backup(self, options: Dict = {}):
        """
        :options:
        Key: db_file:str Source db absolute file path
        Key: db_file_backup:str Destination db absolute file path
        """
        for instance, i_options in self._engines(_get_engine_options(options)):
            try:
                instance.logger.info(f"Backup db: started")
                self._backup(instance=instance, options=i_options)
                instance.logger.info(f"Backup db: completed")
            except BaseException:
                instance.logger.error(f"Backup db: failed", exc_info=1)
                raise

    def _backup(self, instance: SQLAlchemyDBConfig = None, options: Dict = {}):
        raise NotImplementedError("Must be implemented by sub class")

    def dispose(self, options: Dict = {}):
        for instance, i_options in self._engines(_get_engine_options(options)):
            if instance.engine is not None:
                self._dispose(engine=instance.engine)
                self._instances.pop(instance.identifier)

    def _dispose(self, engine: object = None):
        if engine is not None:
            engine.dispose()

    def _setup_engine_session_maker(self, instance: SQLAlchemyDBConfig = None):
        instance.session_maker = self._create_session_maker(
            type=SessionType.MONO_ENGINE, bind=instance.engine, autoflush=True, autocommit=False
        )

    def _setup_multi_engine_session_maker(self, **kwargs):
        return self._create_session_maker(type=SessionType.MULTI_ENGINE, **kwargs)

    def _create_session_maker(self, type: SessionType = SessionType.UNKNOWN, **kwargs):
        session_class = self._get_session_class(type=type)
        return sessionmaker(class_=session_class, **kwargs)

    def _get_session_class(self, type: SessionType = SessionType.UNKNOWN) -> Session.__class__:
        return MultiEngineSession

    @contextmanager
    def session_scope(self, auto_flush=True, expire_on_commit=True):
        """Provide a transactional scope around a series of operations."""
        session_maker = self._setup_multi_engine_session_maker(
            autoflush=auto_flush, expire_on_commit=expire_on_commit
        )

        for session in self._session_scope(session_maker=session_maker):
            yield session

    def _session_scope(self, session_maker=None) -> Generator[Session, None, None]:
        for session in session_scope(
            session_maker=session_maker,
            owner=self,
            instances=self._instances,
        ):
            yield session

    @asynccontextmanager
    async def async_session_scope(self, auto_flush=True, expire_on_commit=True):
        """Provide a transactional scope around a series of operations."""
        session_maker = self._setup_multi_engine_session_maker(
            autoflush=auto_flush, expire_on_commit=expire_on_commit
        )

        for session in self._async_session_scope(session_maker=session_maker):
            yield session

    async def _async_session_scope(
        self, session_maker: None
    ) -> AsyncGenerator[Session, None, None]:
        async for session in async_session_scope(
            session_maker=session_maker,
            owner=self,
            instances=self._instances,
        ):
            yield session
