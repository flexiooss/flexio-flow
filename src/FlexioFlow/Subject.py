from enum import Enum, unique


@unique
class Subject(Enum):
    CORE: str = 'core'
    ISSUE: str = 'issue'
    SCHEME: str = 'scheme'
    VERSION: str = 'version'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))
