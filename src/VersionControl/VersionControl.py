from __future__ import annotations
import abc
from typing import Optional, List

from FlexioFlow.StateHandler import StateHandler
from VersionControl import Commit
from VersionControl.Branch import Branch as VersionControlBranch
from Branches.Branches import Branches
from VersionControl.CommitHandler import CommitHandler
from Core.ConfigHandler import ConfigHandler

class VersionControl:

    def __init__(self, state_handler: StateHandler, config_handler: ConfigHandler):
        self.state_handler: StateHandler = state_handler
        self.config_handler: ConfigHandler = config_handler

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
    def get_issue_number(self) -> Optional[int]:
        pass

    @abc.abstractmethod
    def get_topics_number(self) -> Optional[List[int]]:
        pass

    @abc.abstractmethod
    def commit(self, commit: Commit) -> CommitHandler:
        pass

    @abc.abstractmethod
    def is_current_branch_develop(self) -> bool:
        pass

    @abc.abstractmethod
    def stash_start(self):
        pass

    @abc.abstractmethod
    def stash_end(self):
        pass
