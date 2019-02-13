from enum import Enum, unique


@unique
class VersionController(Enum):
    GIT: str = 'GIT'
