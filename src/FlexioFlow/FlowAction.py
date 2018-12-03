from enum import Enum, unique


@unique
class FlowAction(Enum):
    INIT: str = 'init'
    START: str = 'start'
    FINISH: str = 'finish'
    PLAN: str = 'plan'
