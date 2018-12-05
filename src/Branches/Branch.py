from __future__ import annotations
import abc
from FlexioFlow.FlowAction import FlowAction
from FlexioFlow.StateHandler import StateHandler
from typing import Type


class Branch(abc.ABC):
    action: FlowAction

    def __init__(self, state_handler: StateHandler) -> None:
        self.state_handler: StateHandler = state_handler

    @abc.abstractmethod
    def process(self):
        pass

    def set_action(self, action: FlowAction) -> Branch:
        self.action: FlowAction = action
        return self
