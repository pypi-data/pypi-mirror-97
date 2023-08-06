from typing import Dict

from sqlalchemy.exc import UnboundExecutionError
from sqlalchemy.orm import Session

from constellate.database.sqlalchemy.sqlalchemydbconfig import SQLAlchemyDBConfig


class MultiEngineSession(Session):
    def __init__(self, owner=None, instances: Dict[str, SQLAlchemyDBConfig] = {}, **kwargs):
        super().__init__(**kwargs)
        self._owner = owner
        self._instances = instances

    def get_bind(self, mapper=None, clause=None):
        try:
            return super().get_bind(mapper=mapper, clause=clause)
        except UnboundExecutionError:
            return self._get_bind(mapper=mapper, clause=clause)

    def _get_bind(self, mapper=None, clause=None):
        raise NotImplementedError()
