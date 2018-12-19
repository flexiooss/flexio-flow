from enum import Enum, unique


@unique
class IssueState(Enum):
    OPEN: str = 'open'
    CLOSED: str = 'closed'
