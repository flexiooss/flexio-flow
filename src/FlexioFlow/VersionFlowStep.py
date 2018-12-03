from enum import Enum, unique


@unique
class VersionFlowStep(Enum):
    HOTFIX: str = 'hotfix'
    RELEASE: str = 'release'
