from enum import Enum, unique


@unique
class VersionController(Enum):
    GITFLOW: str = 'GITFLOW'
