from __future__ import annotations

from typing import Type, Optional, List
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
from VersionControlProvider.Topic import Topic
from Core.ConfigHandler import ConfigHandler


class Start:

    def __init__(self, state_handler: StateHandler, config_handler: ConfigHandler, issue: Optional[Issue],
                 topics: Optional[List[Topic]], name: str):
        self.__state_handler: StateHandler = state_handler
        self.__config_handler: ConfigHandler = config_handler
        self.__issue: Optional[Issue] = issue
        self.__topics: Optional[List[Topic]] = topics
        self.__name: str = slugify(name)
        self.__git: GitCmd = GitCmd(self.__state_handler).with_config_handler(config_handler)
        self.__gitflow: GitFlowCmd = GitFlowCmd(self.__state_handler, self.__config_handler)

    def __init_gitflow(self) -> Start:
        self.__gitflow.init_config()
        return self

    def __pull_develop(self) -> Start:
        self.__git.checkout(self.__config_handler.develop()).try_to_pull()
        return self

    def __start_feature(self):
        self.__git.checkout(self.__config_handler.develop())
        branch_name: str = BranchHandler(self.__config_handler.feature(),
                                         self.__config_handler.config.branches_config).with_issue(
            self.__issue).with_topics(
            self.__topics).branch_name_from_version_with_name(
            version=self.__state_handler.state.version,
            name=self.__name
        )

        if self.__git.branch_exists(branch_name):
            raise BranchAlreadyExist(self.__config_handler.feature(), branch_name)

        self.__git.create_branch_from(branch_name, self.__config_handler.develop())

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
