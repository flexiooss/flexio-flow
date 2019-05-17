from __future__ import annotations

from typing import Type, Optional
from slugify import slugify

from Exceptions.BranchAlreadyExist import BranchAlreadyExist
from Exceptions.NotCleanWorkingTree import NotCleanWorkingTree
from FlexioFlow.StateHandler import StateHandler
from Branches.BranchHandler import BranchHandler
from Branches.Branches import Branches
from VersionControl.Git.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.Git.GitCmd import GitCmd
from VersionControlProvider.Github.Message import Message
from VersionControlProvider.Issue import Issue


class Start:

    def __init__(self, state_handler: StateHandler, issue: Optional[Issue], name: str):
        self.__state_handler: StateHandler = state_handler
        self.__issue: Optional[Issue] = issue
        self.__name: str = slugify(name)
        self.__git: GitCmd = GitCmd(self.__state_handler)
        self.__gitflow: GitFlowCmd = GitFlowCmd(self.__state_handler)

    def __init_gitflow(self) -> Start:
        self.__gitflow.init_config()
        return self

    def __pull_develop(self) -> Start:
        self.__git.checkout(Branches.DEVELOP).try_to_pull()
        return self

    def __start_feature(self):
        self.__git.checkout(Branches.DEVELOP)
        branch_name: str = BranchHandler(Branches.FEATURE).with_issue(self.__issue).branch_name_from_version_with_name(
            version=self.__state_handler.state.version,
            name=self.__name
        )

        if self.__git.branch_exists(branch_name):
            raise BranchAlreadyExist(Branches.FEATURE, branch_name)

        self.__git.create_branch_from(branch_name, Branches.DEVELOP)

        self.__git.commit(
            Message(
                message=''.join(["'Start feature : ", branch_name, "'"]),
                issue=self.__issue
            ).with_ref()
        ).try_to_set_upstream()

    def process(self):
        if not self.__git.is_clean_working_tree():
            raise NotCleanWorkingTree()
        self.__init_gitflow().__pull_develop().__start_feature()
