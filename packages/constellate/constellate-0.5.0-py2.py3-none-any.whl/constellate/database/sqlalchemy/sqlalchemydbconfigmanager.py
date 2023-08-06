from constellate.database.sqlalchemy.sqlalchemydbconfig import SQLAlchemyDBConfig, DBConfigType


class SQLAlchemyDbConfigManager:
    def __init__(self):
        self._instances = {}

    def update(self, instance: SQLAlchemyDBConfig = None):
        self._instances.update({instance.identifier: instance})

    def pop(self, identifier: str = None):
        self._instances.pop(identifier)

    def __iter__(self):
        return self._instances.items().__iter__()

    def get(self, identifier: str = None, default_value=None):
        return self._insances.get(identifier, default_value)

    def find(self, type: DBConfigType = DBConfigType.INSTANCE, identifier: str = None):
        return next(
            filter(
                lambda config: config.type == type and config.identifier == identifier,
                self._instances.values(),
            ),
            None,
        )
