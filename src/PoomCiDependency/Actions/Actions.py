from enum import Enum, unique


@unique
class Actions(Enum):
    FULL_REPOSITORY_JSON: str = 'full-repository-json'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))
