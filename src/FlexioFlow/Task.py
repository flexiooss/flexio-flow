from enum import Enum, unique


@unique
class Task(Enum):
    BRANCH: str = 'branch'
    CORE: str = 'core'
    ISSUE: str = 'issue'
    TOPICS: str = 'topics'
    SCHEME: str = 'scheme'
    VERSION: str = 'version'
    CONVERT: str = 'convert'
    POOM_CI: str = 'poom-ci'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))
