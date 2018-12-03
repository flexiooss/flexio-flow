from enum import Enum, unique


@unique
class Level(Enum):
    DEV: str = 'dev'
    STABLE: str = 'stable'
