from typing import Dict, Tuple

from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy_utils import database_exists

from constellate.database.migration.databasetype import DatabaseType
from constellate.database.migration.migrate import migrate
from constellate.database.migration.migrationaction import MigrationAction
from constellate.database.sqlalchemy.sqlalchemy import SQLAlchemy
from constellate.database.sqlalchemy.sqlalchemydbconfig import SQLAlchemyDBConfig

_POOL_CONNECTION_PERMANENT_SIZE = 10
_POOL_CONNECTION_OVERFLOW_SIZE = 5


class SQLAlchemyPostgresql(SQLAlchemy):
    def __init__(self):
        super().__init__()

    def _create_engine(self, options: Dict = {}) -> Tuple[str, object]:
        """
        :options:
        - host:str               . DB host
        - port:str               . DB port
        - username:str           . DB user name
        - password:str           . DB password
        - db_name:str            . DB name
        - pool_connection_size:int            . Max permanent connection held in the pool. Default: 10
        - pool_connection_overflow_size:int            . Max connection returned in addition to the ones in the pool. Default: 5
        - pool_connection_timeout:float . Max timeout to return a connection, in seconds. Default: 30.0 (sec)
        - custom: Dict[any,any]. Dictionary of custom attribute, never used by constellate
        """
        # Create engine
        # - https://docs.sqlalchemy.org/en/14/dialects/postgresql.html
        connection_uri_no_scheme_no_db_name = (
            f"{options.get('username', None)}:{options.get('password', None)}@"
            f"{options.get('host', None)}:{options.get('port', None)}"
        )

        connection_uri = (
            f"postgresql://{connection_uri_no_scheme_no_db_name}/{options.get('db_name', None)}"
        )
        if not database_exists(connection_uri):
            self._create_database(
                connection_uri=f"postgresql://{connection_uri_no_scheme_no_db_name}",
                db_name=options.get("db_name", None),
            )

        pool_size = options.get("pool_connection_size", 10)
        pool_overflow_size = options.get("pool_connection_overflow_size", 5)
        pool_timeout = options.get("pool_connection_timeout", 30.0)

        engine = create_engine(
            connection_uri,
            poolclass=QueuePool,
            pool_size=pool_size,
            max_overflow=pool_overflow_size,
            pool_timeout=pool_timeout,
        )
        return connection_uri, engine

    def _create_database(self, connection_uri: str = None, db_name: str = None, encoding="UTF8"):
        with create_engine(connection_uri, isolation_level="AUTOCOMMIT").connect() as connection:
            connection.execute(f"CREATE DATABASE {db_name} ENCODING {encoding};")

    def _migrate(self, instance: SQLAlchemyDBConfig = None, options: Dict = {}):
        migrate(
            database_type=DatabaseType.POSTGRESQL,
            connection_url=instance.connection_uri,
            migration_dirs=options.get("migration_dirs", []),
            action=MigrationAction.UP,
            logger=instance.logger,
        )

    def _vacuum(self, instance: SQLAlchemyDBConfig = None, options: Dict = {}):
        """
        :options:
        - profiles: A vacumm profile. Values:
        -- analyze: Updates statistics used by the planner (to speed up queries)
        -- default: Sensible defaults
        """
        # Vacuum requires a connection/session without transaction enabled.
        with instance.engine.connect().execution_options(
            isolation_level="AUTOCOMMIT"
        ) as connection:
            commands = {
                "analyze": ["VACUUM ANALYZE;"],
                "default": ["VACUUM (ANALYZE, VERBOSE);"],
            }
            for profile in options.get("profiles", ["default"]):
                for statement in commands[profile]:
                    try:
                        connection.execute(statement)
                    except BaseException as e:
                        raise Exception(f"Vacuum statement failed: {statement}") from e
