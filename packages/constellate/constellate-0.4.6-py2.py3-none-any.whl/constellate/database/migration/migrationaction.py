from enum import Enum, auto


class MigrationAction(Enum):
    UNKNOWN = auto()
    UP = auto()
    DOWN = auto()
