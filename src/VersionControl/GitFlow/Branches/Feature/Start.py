from __future__ import annotations

from typing import Type, Optional
from slugify import slugify
from FlexioFlow.StateHandler import StateHandler
from Branches.BranchHandler import BranchHandler
from Branches.Branches import Branches
from VersionControl.GitFlow.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.GitFlow.GitCmd import GitCmd
from VersionControlProvider.Github.Message import Message
from VersionControlProvider.Issue import Issue


class Start:

    def __init__(self, state_handler: StateHandler, issue: Optional[Type[Issue]], name: str):
        self.__state_handler: StateHandler = state_handler
        self.__issue: Optional[Issue] = issue
        self.__name: str = slugify(name)
        self.__git: GitCmd = GitCmd(self.__state_handler)
        self.__gitflow: GitFlowCmd = GitFlowCmd(self.__state_handler)

    def __init_gitflow(self) -> Start:
        self.__gitflow.init_config()
        return self

    def __pull_develop(self) -> Start:
        self.__git.checkout(Branches.DEVELOP).pull()
        return self

    def __pull_master(self) -> Start:
        self.__git.checkout(Branches.MASTER).pull()
        return self

    def __start_feature(self):
        self.__git.checkout(Branches.DEVELOP)
        branch_name: str = BranchHandler(Branches.FEATURE).with_issue(self.__issue).branch_name_from_version_with_name(
            version=self.__state_handler.state.version,
            name=self.__name
        )

        self.__git.create_branch_from(branch_name, Branches.DEVELOP)

        self.__git.commit(
            Message(
                message=''.join(["'Start feature : ", branch_name, "'"]),
                issue=self.__issue
            ).with_ref()
        ).set_upstream()

    def process(self):
        self.__init_gitflow().__pull_develop().__pull_master().__start_feature()
