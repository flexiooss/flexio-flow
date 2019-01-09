from enum import Enum, unique


@unique
class IssueActions(Enum):
    READ: str = 'read'
    COMMENT: str = 'comment'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))
