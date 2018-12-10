from __future__ import annotations
import abc
from FlexioFlow.StateHandler import StateHandler
from VersionControl.Branch import Branch
from VersionControl.Branches import Branches
from typing import Type


class VersionControl:

    def __init__(self, state_handler: StateHandler):
        self.state_handler: StateHandler = state_handler

    @abc.abstractmethod
    def hotfix(self) -> Branch:
        pass

    @abc.abstractmethod
    def release(self) -> Branch:
        pass

    @abc.abstractmethod
    def with_branch(self, branch: Branches) -> Branch:
        pass
