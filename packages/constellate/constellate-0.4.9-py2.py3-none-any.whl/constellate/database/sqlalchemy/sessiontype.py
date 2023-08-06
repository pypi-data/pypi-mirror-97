from enum import Enum, auto


class SessionType(Enum):
    UNKNOWN = auto()
    MONO_ENGINE = auto()
    MULTI_ENGINE = auto()
