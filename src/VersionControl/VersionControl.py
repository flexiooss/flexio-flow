from __future__ import annotations
import abc
from FlexioFlow.StateHandler import StateHandler


class VersionControl:

    def __init__(self, state_handler: StateHandler):
        self.state_handler: StateHandler = state_handler

    @abc.abstractmethod
    def hotfix(self):
        pass

    @abc.abstractmethod
    def release(self):
        pass
