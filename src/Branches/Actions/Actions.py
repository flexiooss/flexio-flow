from enum import Enum, unique


@unique
class Actions(Enum):
    COMMIT: str = 'commit'
    FINISH: str = 'finish'
    INIT: str = 'init'
    PRECHECK: str = 'precheck'
    START: str = 'start'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))
