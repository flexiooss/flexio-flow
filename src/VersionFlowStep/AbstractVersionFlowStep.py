import abc
from FlexioFlow import FlowAction


class AbstractVersionFlowStep(abc.ABC):
    action: FlowAction

    @abc.abstractmethod
    def process(self):
        pass
