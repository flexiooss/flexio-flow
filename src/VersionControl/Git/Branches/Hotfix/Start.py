from __future__ import annotations

from typing import Type, Optional, List

from Exceptions.BranchAlreadyExist import BranchAlreadyExist
from Exceptions.NotCleanWorkingTree import NotCleanWorkingTree
from FlexioFlow.StateHandler import StateHandler
from Schemes.UpdateSchemeVersion import UpdateSchemeVersion
from Branches.BranchHandler import BranchHandler
from Branches.Branches import Branches
from VersionControl.Git.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.Git.GitCmd import GitCmd
from VersionControlProvider.Github.Message import Message
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic
from Core.ConfigHandler import ConfigHandler


class Start:
    def __init__(self,
                 state_handler: StateHandler,
                 config_handler: ConfigHandler,
                 issue: Optional[Type[Issue]],
                 topics: Optional[List[Topic]]
                 ):
        self.__state_handler: StateHandler = state_handler
        self.__config_handler: ConfigHandler = config_handler
        self.__issue: Optional[Type[Issue]] = issue
        self.__topics: Optional[List[Topic]] = topics
        self.__git: GitCmd = GitCmd(self.__state_handler).with_config_handler(config_handler)
        self.__gitflow: GitFlowCmd = GitFlowCmd(self.__state_handler,config_handler)

    def __init_gitflow(self) -> Start:
        self.__gitflow.init_config()
        return self

    def __pull_develop(self) -> Start:
        self.__git.checkout(self.__config_handler.develop()).try_to_pull()
        return self

    def __pull_master(self) -> Start:
        self.__git.checkout(self.__config_handler.master()).try_to_pull()
        return self

    def __start_hotfix(self):
        if self.__gitflow.has_release(True) or self.__gitflow.has_release(False):
            raise BranchAlreadyExist(self.__config_handler.release())
        if self.__gitflow.has_hotfix(True) or self.__gitflow.has_hotfix(False):
            raise BranchAlreadyExist(self.__config_handler.hotfix())

        self.__git.checkout(self.__config_handler.master())
        branch_name: str = BranchHandler(self.__config_handler.hotfix(),self.__config_handler.config.branches_config).with_issue(self.__issue).with_topics(
            self.__topics).branch_name_from_version(
            self.__state_handler.get_next_patch_version())

        self.__git.create_branch_from(branch_name, self.__config_handler.master())

        self.__state_handler.next_dev_patch()
        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)
        self.__git.commit(
            Message(
                message="'Start hotfix : {branch_name!s}'".format(branch_name=branch_name),
                issue=self.__issue
            ).with_ref()
        ).try_to_set_upstream()

    def process(self):
        if not self.__git.is_clean_working_tree():
            raise NotCleanWorkingTree()
        self.__init_gitflow().__pull_develop().__pull_master().__start_hotfix()
