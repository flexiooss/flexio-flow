from enum import Enum, unique


@unique
class TopicActions(Enum):
    READ: str = 'read'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))
