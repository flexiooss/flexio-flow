from FlexioFlowObjectHandler import FlexioFlowObjectHandler
from enum import Enum, unique


@unique
class FlowAction(Enum):
    INIT: str = 'init'
    START: str = 'start'
    FINISH: str = 'finish'
    PLAN: str = 'plan'


@unique
class VersionFlowStep(Enum):
    HOTFIX: str = 'hotfix'
    RELEASE: str = 'release'


class FlexioFlow:
    config: FlexioFlowObjectHandler
    step: VersionFlowStep
    action: FlowAction

    def __init__(self):
        pass

    def initContext(self):
        pass
