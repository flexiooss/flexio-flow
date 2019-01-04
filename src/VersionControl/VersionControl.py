from __future__ import annotations
import abc
from typing import Optional

from FlexioFlow.StateHandler import StateHandler
from VersionControl.Branch import Branch as VersionControlBranch
from Branches.Branches import Branches
from VersionControlProvider.Issue import Issue


class VersionControl:

    def __init__(self, state_handler: StateHandler):
        self.state_handler: StateHandler = state_handler

    @abc.abstractmethod
    def hotfix(self) -> VersionControlBranch:
        pass

    @abc.abstractmethod
    def release(self) -> VersionControlBranch:
        pass

    @abc.abstractmethod
    def feature(self) -> VersionControlBranch:
        pass

    @abc.abstractmethod
    def build_branch(self, branch: Branches) -> VersionControlBranch:
        pass

    @abc.abstractmethod
    def get_issue_number(self) -> Optional[Issue]:
        pass
