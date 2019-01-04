from enum import Enum, unique


@unique
class Actions(Enum):
    INIT: str = 'init'
    FINISH: str = 'finish'
    PRECHECK: str = 'precheck'
    START: str = 'start'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))
