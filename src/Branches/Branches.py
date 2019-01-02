from enum import Enum, unique


@unique
class Branches(Enum):
    DEVELOP: str = 'develop'
    FEATURE: str = 'feature'
    HOTFIX: str = 'hotfix'
    MASTER: str = 'master'
    RELEASE: str = 'release'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))
