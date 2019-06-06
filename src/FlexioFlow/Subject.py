from enum import Enum, unique


@unique
class Subject(Enum):
    BRANCH: str = 'branch'
    CORE: str = 'core'
    ISSUE: str = 'issue'
    TOPIC: str = 'topic'
    SCHEME: str = 'scheme'
    VERSION: str = 'version'
    POOM_CI: str = 'poom-ci'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))
