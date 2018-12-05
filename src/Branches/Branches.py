from enum import Enum, unique


@unique
class Branches(Enum):
    HOTFIX: str = 'hotfix'
    RELEASE: str = 'release'
