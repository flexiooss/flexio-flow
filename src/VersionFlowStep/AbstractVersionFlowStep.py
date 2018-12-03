import abc
from FlexioFlow.FlowAction import FlowAction


class AbstractVersionFlowStep(abc.ABC):
    action: FlowAction

    @abc.abstractmethod
    def process(self):
        pass
