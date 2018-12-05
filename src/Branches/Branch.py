from __future__ import annotations
import abc
from FlexioFlow.FlowAction import FlowAction
from typing import Type


class Branch(abc.ABC):
    action: FlowAction

    @abc.abstractmethod
    def process(self):
        pass

    def set_action(self, action: FlowAction) -> Branch:
        self.action = action
        return self
