from __future__ import annotations
from typing import Type, Optional
from Exceptions.BranchAlreadyExist import BranchAlreadyExist
from Exceptions.NotCleanWorkingTree import NotCleanWorkingTree
from Exceptions.RemoteDivergence import RemoteDivergence
from FlexioFlow.StateHandler import StateHandler
from Schemes.UpdateSchemeVersion import UpdateSchemeVersion
from Branches.BranchHandler import BranchHandler
from Branches.Branches import Branches
from VersionControl.Git.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.Git.GitCmd import GitCmd
from VersionControlProvider.Github.Message import Message
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic


class Start:
    def __init__(self,
                 state_handler: StateHandler,
                 issue: Optional[Type[Issue]],
                 topic: Optional[Topic],
                 is_major: bool
                 ):
        self.__state_handler: StateHandler = state_handler
        self.__issue: Optional[Type[Issue]] = issue
        self.__topic: Optional[Topic] = topic
        self.__is_major: bool = is_major
        self.__git: GitCmd = GitCmd(self.__state_handler)
        self.__gitflow: GitFlowCmd = GitFlowCmd(self.__state_handler)

    def __init_gitflow(self) -> Start:
        self.__gitflow.init_config()
        return self

    def __pull_develop(self) -> Start:
        self.__git.checkout(Branches.DEVELOP).try_to_pull()
        return self

    def __pull_master(self) -> Start:
        self.__git.checkout(Branches.MASTER).try_to_pull()
        return self

    def __set_version(self):
        if self.__is_major:
            self.__state_handler.next_major()

    def __start_check(self):
        #  TODO recheck local vs remote
        # if self.__git.has_remote() and not self.__git.is_local_remote_equal(Branches.DEVELOP.value):
        #     raise RemoteDivergence(Branches.DEVELOP.value)

        if not self.__git.is_clean_working_tree():
            raise NotCleanWorkingTree('Stash or commit your changes !!!')

        if self.__gitflow.has_release(True) or self.__gitflow.has_release(False):
            raise BranchAlreadyExist(Branches.RELEASE)

        if self.__gitflow.has_hotfix(True) or self.__gitflow.has_hotfix(False):
            raise BranchAlreadyExist(Branches.HOTFIX)

    def __start_release(self):
        self.__start_check()

        self.__git.checkout(Branches.DEVELOP)
        self.__set_version()

        branch_name: str = BranchHandler(Branches.RELEASE).with_issue(self.__issue).with_topic(
            self.__topic).branch_name_from_version(
            self.__state_handler.state.version
        )

        self.__git.create_branch_from(branch_name, Branches.DEVELOP)

        self.__set_version()
        self.__state_handler.set_stable()
        self.__state_handler.write_file()

        UpdateSchemeVersion.from_state_handler(self.__state_handler)

        self.__git.commit(
            Message(
                message=''.join(["'Start release : ", branch_name, "'"]),
                issue=self.__issue
            ).with_ref()
        ).try_to_set_upstream()

    def process(self):
        if not self.__git.is_clean_working_tree():
            raise NotCleanWorkingTree()
        self.__init_gitflow().__pull_develop().__pull_master().__start_release()
