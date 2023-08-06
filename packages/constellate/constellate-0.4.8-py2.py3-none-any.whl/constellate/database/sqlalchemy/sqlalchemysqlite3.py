from contextlib import contextmanager
from sqlite3.dbapi2 import Connection
from typing import Dict, Tuple

from sqlalchemy import create_engine, event
from sqlalchemy.pool import NullPool

from constellate.database.migration.databasetype import DatabaseType
from constellate.database.migration.migrate import migrate
from constellate.database.migration.migrationaction import MigrationAction
from constellate.database.sqlalchemy.sqlalchemy import SQLAlchemy
from constellate.database.sqlalchemy.sqlalchemydbconfig import SQLAlchemyDBConfig
from constellate.database.sqlite3.sqlite3 import patch_sqlite3_connect
from constellate.database.sqlite3.sqlite3 import register_functions, Functions


@contextmanager
def raw_sqlite3_connection(engine, issue_begin=True, issue_commit_or_rollback=True, close=True):
    try:
        connection = engine.raw_connection()
        if issue_begin:
            connection.execute("BEGIN")
        yield connection
        # Caller will execute series of sql commands
        if issue_commit_or_rollback:
            connection.commit()
    except BaseException:
        if issue_commit_or_rollback:
            connection.rollback()
    finally:
        if close and connection is not None:
            connection.close()


class SQLAlchemySqlite3(SQLAlchemy):
    def __init__(self):
        super().__init__()

    def _create_engine(self, options: Dict = {}) -> Tuple[str, object]:
        """
        :options:
        - db_file:str           . Absolute db file path
        - check_same_thread:bool. Default False
        - timeout:int           . Default 20s
        - uri:bool              . Default: True
        """
        # Create engine
        # - https://docs.sqlalchemy.org/en/14/dialects/sqlite.html?highlight=isolation_level#using-temporary-tables-with-sqlite
        # - https://docs.sqlalchemy.org/en/14/dialects/sqlite.html?highlight=isolation_level#threading-pooling-behavior
        connection_uri = (
            f"sqlite:///{options.get('db_file', None)}?check_same_thread=false&timeout=20&uri=true"
        )

        # To see commit statement: add echo=True, echo_pool=True
        engine = create_engine(connection_uri, poolclass=NullPool)
        return connection_uri, engine

    def _setup_engine_connection_connect(self, engine=None, options: Dict = None):
        # 2. Improve default db performance, per connection
        @event.listens_for(engine, "connect")
        def improve_perf_on_connection_start(dbapi_connection, connection_record):
            if isinstance(dbapi_connection, Connection):
                # Prevent python sdk's pysqlite's from emitting BEGIN statement entirely
                # Also prevent pysqlite from emitting COMMIT before any DDL statement
                dbapi_connection.isolation_level = None
                cursor = dbapi_connection.cursor()
                # src: https://phiresky.github.io/blog/2020/sqlite-performance-tuning/
                for pragma in [
                    "pragma journal_mode = WAL;",
                    "pragma synchronous = normal;",
                    "pragma temp_store = memory;",
                ]:
                    cursor.execute(pragma)
                cursor.close()

    def _setup_engine_connection_begin(self, engine=None, options: Dict = None):
        """
        :options:
        - Key: functions:Dict. Eg: {'my_custom_function': (1, lambda foo: return random_stuff)}
        """
        # Register custom SQL function
        @event.listens_for(engine, "begin")
        def do_begin(conn):
            conn.execute(
                "BEGIN -- Note: BEGIN(implicty) (in the sqlalchemy engine logs) means SQLAlchemy considers this moment to be the start of a transaction block BUT did not send any BEGIN statement to the database. Hence the explicit: BEGIN"
            )
            functions = options.get("functions", {})
            register_functions(connection=conn.connection, functions=functions)

    def _migrate(self, instance: SQLAlchemyDBConfig = None, options: Dict = {}):
        migrate(
            database_type=DatabaseType.SQLITE,
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
        # src: https://phiresky.github.io/blog/2020/sqlite-performance-tuning/
        with raw_sqlite3_connection(
            instance.engine, issue_begin=True, issue_commit_or_rollback=True, close=True
        ) as connection:
            pragma = "pragma wal_checkpoint(TRUNCATE);"
            cursor = connection.execute(pragma)
            data = cursor.fetchone()
            if data is None or len(data) == 0:
                raise Exception(f"{pragma} failed: {data}")

            pragma = "pragma vacuum;"
            cursor = connection.execute(pragma)
            data = cursor.fetchone()
            if data is not None:
                raise Exception(f"{pragma} failed")

            pragma = "pragma integrity_check;"
            cursor = connection.execute(pragma)
            data = cursor.fetchone()
            if data is None or data[0] != "ok":
                raise Exception(f"{pragma} failed: {data}")

            # pragma = "pragma foreign_key_check;"
            # cursor = connection.execute(pragma)
            # if ???:
            #     raise Exception(f"{pragma} failed")

    def _backup(self, instance: SQLAlchemyDBConfig = None, options: Dict = {}):
        """
        options:
        -Key: db_file:str. Absolute path to source db file
        -Key: db_file_backup:str. Absolute path to destination db file
        """

        def progress(status, remaining, total):
            instance.logger.debug(f"{status}: Backing up {total - remaining} of {total} pages...")

        try:
            import sqlite3

            db_file = options.get("db_file", None)
            db_file_backup = options.get("db_file_backup", None)

            connection_src = sqlite3.connect(db_file)
            connection_dst = sqlite3.connect(db_file_backup)
            with connection_dst:
                connection_src.backup(connection_dst, pages=10000, progress=progress)
                connection_dst.commit()
            connection_dst.close()
            connection_src.close()
        except BaseException:
            # FIXME delete backup
            raise

    def monkeypatch_sqlite3_connect(self, enable: bool = True, functions: Functions = {}):
        import _sqlite3

        patch_sqlite3_connect(original_connect=_sqlite3.connect, enable=enable, functions=functions)
