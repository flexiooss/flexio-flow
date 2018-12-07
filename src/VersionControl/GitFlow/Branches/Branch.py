from __future__ import annotations
import abc
from FlexioFlow.Actions.Actions import Actions
from FlexioFlow.StateHandler import StateHandler


class Branch(abc.ABC):
    action: Actions

    def __init__(self, state_handler: StateHandler) -> None:
        self.state_handler: StateHandler = state_handler

    @abc.abstractmethod
    def process(self):
        pass

    def set_action(self, action: Actions) -> Branch:
        self.action: Actions = action
        return self
