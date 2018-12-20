from __future__ import annotations
import abc
from FlexioFlow.StateHandler import StateHandler
from VersionControl.Branch import Branch
from Branches.Branches import Branches
from typing import Optional

from VersionControlProvider.Github.IssueGithub import IssueGithub


class VersionControl:

    def __init__(self, state_handler: StateHandler):
        self.state_handler: StateHandler = state_handler
        self.issue: Optional[IssueGithub] = None

    def with_issue(self, issue: IssueGithub) -> VersionControl:
        self.issue = issue
        return self

    @abc.abstractmethod
    def hotfix(self) -> Branch:
        pass

    @abc.abstractmethod
    def release(self) -> Branch:
        pass

    @abc.abstractmethod
    def feature(self) -> Branch:
        pass

    @abc.abstractmethod
    def with_branch(self, branch: Branches) -> Branch:
        pass
