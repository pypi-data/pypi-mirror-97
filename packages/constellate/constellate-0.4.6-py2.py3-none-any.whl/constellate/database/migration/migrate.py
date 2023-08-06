import logging
from logging import getLogger
from pathlib import Path
from typing import List

from yoyo import read_migrations
from yoyo import get_backend

from constellate.database.migration.databasetype import DatabaseType
from constellate.database.migration.migrationaction import MigrationAction
from constellate.database.migration.migrationerror import MigrationException


def _migrate_with_yoyo(
    connection_url: str = None,
    migration_dirs: List[Path] = [],
    action: MigrationAction = MigrationAction.UNKNOWN,
    logger: logging.Logger = None,
):
    """Run database migrations using yoyo library: https://ollycope.com/software/yoyo/latest/#migrations-as-sql-scripts"""

    class Handler(logging.Handler):
        def __init__(self, level: int = logging.NOTSET, target_logger: logging.Logger = None):
            super(Handler, self).__init__(level=level)
            self._target_logger = target_logger

        def emit(self, record: logging.LogRecord) -> None:
            if self._target_logger is not None:
                self._target_logger.log(level=record.levelno, msg=record.getMessage())

        def flush(self) -> None:
            if self._target_logger is not None:
                self._target_logger.flush()

    handler = Handler(level=logging.DEBUG, target_logger=logger)
    # Append temporary Handler to yoyo's library
    yoyo_logger = getLogger("yoyo.migrations")
    yoyo_logger.setLevel(logging.DEBUG)

    backend = None
    try:
        yoyo_logger.addHandler(handler)

        # Run migration
        backend = get_backend(connection_url)
        migrations = read_migrations(*[str(path) for path in migration_dirs])

        with backend.lock():
            if action == MigrationAction.UP:
                # Apply any outstanding migrations
                backend.apply_migrations(backend.to_apply(migrations))
            elif action == MigrationAction.DOWN:
                # Rollback all migrations
                backend.rollback_migrations(backend.to_rollback(migrations))
    except BaseException:
        raise
    finally:
        # Remove lock, regardless of migration status
        if backend is not None:
            backend.break_lock()
        yoyo_logger.removeHandler(handler)


def _migrate_unsupported(
    connection_url: str = None,
    migration_dirs: List[Path] = [],
    action: MigrationAction = MigrationAction.UNKNOWN,
    logger: logging.Logger = None,
):
    raise NotImplementedError()


def migrate(
    database_type: DatabaseType = DatabaseType.UNKNOWN,
    connection_url: str = None,
    migration_dirs: List[Path] = [],
    action: MigrationAction = MigrationAction.UNKNOWN,
    logger: logging.Logger = None,
):
    """Run database migrations.
    :migration_dirs: List of directory contains SQL file scripts (or equivalent)
                     SQL file scripts must be named with script alphabetic order:
                     - 0001.up.foobar.sql
                     - 0001.down.foobar.sql
                     - 0002.up.zoobar.sql
                     - etc ...
    :raises:
        MigrationException When migration fails
    """
    DB_TYPE_TO_MIGRATOR = {
        DatabaseType.SQLITE: _migrate_with_yoyo,
        DatabaseType.POSTGRESQL: _migrate_with_yoyo,
    }

    try:
        migrate = DB_TYPE_TO_MIGRATOR.get(database_type, _migrate_unsupported)
        migrate(
            connection_url=connection_url,
            migration_dirs=migration_dirs,
            action=action,
            logger=logger,
        )
    except BaseException as e:
        raise MigrationException() from e


#
# from pkg_resources import resource_listdir, resource_string
# def migrate2(connection=None, logger=None):
#     """Run database migrations."""
#
#     def get_script_version(filename) -> int:
#         return int(filename.split("_")[0])
#
#     def get_current_version(connection, default_version=9999999):
#         try:
#             current_version = connection.execute("pragma user_version").fetchone()[0]
#             return current_version
#         except BaseException:
#             return default_version
#
#     migrations_parent_pkg_dir = __package__
#     migration_dir_name = "migrations"
#
#     # Retrieve list of incremental migration scripts, sorted by migration number ascending
#     migration_files = resource_listdir(migrations_parent_pkg_dir, migration_dir_name)
#     migration_version_to_files = {get_script_version(file): file for file in migration_files}
#
#     migration_versions = sorted(list(migration_version_to_files.keys()))
#     logger.info(f"{len(migration_versions)} migration scripts available")
#
#     # Apply incremental migration scripts strictly above current db schema version
#     for script_version in migration_versions:
#         script_filename = migration_version_to_files.get(script_version, None)
#
#         current_version = get_current_version(connection)
#         if script_version == current_version:
#             logger.info(f"database currently at version {current_version}")
#
#         if script_version > current_version:
#             logger.debug(f"migration being applied {script_version}")
#             sql = resource_string(
#                 migrations_parent_pkg_dir, f"{migration_dir_name}/{script_filename}"
#             ).decode("utf-8")
#             connection.executescript(sql)
#             new_current_version = get_current_version(connection)
#
#             if new_current_version == script_version:
#                 logger.info(f"database now upgraded to version {script_version}")
#             else:
#                 raise Exception(f"database failed migrate to version {script_version}")
#
#     # Verify the app's db is now at the version of the very last migration script available
#     last_available_migration_version = (
#         migration_versions[-1] if len(migration_versions) > 0 else current_version
#     )
#     assert (
#         current_version == last_available_migration_version
#     ), f"Database not migrated to most up to date version {last_available_migration_version}"
