from enum import Enum, unique


@unique
class GitConfig(Enum):
    REMOTE: str = 'origin'
