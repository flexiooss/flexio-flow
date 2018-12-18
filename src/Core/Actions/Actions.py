from enum import Enum, unique


@unique
class Actions(Enum):
    CONFIG: str = 'config'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))
