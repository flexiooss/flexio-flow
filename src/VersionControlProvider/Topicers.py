from enum import Enum, unique


@unique
class Topicers(Enum):
    FLEXIO: str = 'flexio'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))

