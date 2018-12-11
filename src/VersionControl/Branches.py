from enum import Enum, unique


@unique
class Branches(Enum):
    MASTER: str = 'master'
    DEVELOP: str = 'develop'
    HOTFIX: str = 'hotfix'
    RELEASE: str = 'release'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))
