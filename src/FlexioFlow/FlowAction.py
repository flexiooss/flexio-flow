from enum import Enum, unique


@unique
class FlowAction(Enum):
    INIT: str = 'init'
    START: str = 'start'
    FINISH: str = 'finish'
    PLAN: str = 'plan'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))
