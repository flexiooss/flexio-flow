from __future__ import annotations

from typing import Type, Optional
from Exceptions.BranchNotExist import BranchNotExist
from FlexioFlow.StateHandler import StateHandler
from Branches.Branches import Branches
from VersionControl.GitFlow.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.GitFlow.GitCmd import GitCmd
from VersionControlProvider.Github.Message import Message
from VersionControlProvider.Issue import Issue


class Finish:
    def __init__(self, state_handler: StateHandler, issue: Optional[Type[Issue]]):
        self.__state_handler: StateHandler = state_handler
        self.__issue: Optional[Type[Issue]] = issue
        self.__git: GitCmd = GitCmd(self.__state_handler)
        self.__gitflow: GitFlowCmd = GitFlowCmd(self.__state_handler)
        self.__current_branch_name: str = self.__git.get_current_branch_name()

    def __init_gitflow(self) -> Finish:
        self.__gitflow.init_config()
        return self

    def __pull_develop(self) -> Finish:
        self.__git.checkout(Branches.DEVELOP).pull()
        return self

    def __pull_master(self) -> Finish:
        self.__git.checkout(Branches.MASTER).pull()
        return self

    def __merge_develop(self) -> Finish:
        self.__git.checkout_with_branch_name(self.__current_branch_name)
        self.__git.commit(
            Message(
                message=''.join([
                    "'Finish feature ` ",
                    self.__current_branch_name,
                    " ` for dev: ",
                    self.__state_handler.version_as_str()
                ]),
                issue=self.__issue
            ).with_close()
        ).push()

        self.__git.checkout(Branches.DEVELOP).merge_with_version_message(
            branch=Branches.FEATURE,
            message=Message(
                message='',
                issue=self.__issue
            ).with_ref()
        ).push()

        if self.__git.has_conflict():
            print('##################################################')
            print('develop have conflicts : ')
            print(self.__git.get_conflict())
            print('##################################################')
        return self

    def __delete_feature(self) -> Finish:
        self.__git.delete_branch_from_name(self.__current_branch_name, True)
        self.__git.delete_branch_from_name(self.__current_branch_name, False)
        return self

    def __finish_feature(self):
        self.__git.checkout_file_with_branch_name(Branches.DEVELOP.value, self.__state_handler.file_path())
        self.__merge_develop().__delete_feature()

    def process(self):
        if not self.__gitflow.is_feature():
            raise BranchNotExist(Branches.FEATURE)
        self.__pull_develop().__pull_master().__finish_feature()
