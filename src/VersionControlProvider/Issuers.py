from enum import Enum, unique


@unique
class Issuers(Enum):
    FLEXIO: str = 'flexio'
    GITHUB: str = 'github'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))

