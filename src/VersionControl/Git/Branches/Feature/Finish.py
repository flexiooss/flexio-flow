from __future__ import annotations

from typing import Type, Optional
from Exceptions.BranchNotExist import BranchNotExist
from Exceptions.GitMergeConflictError import GitMergeConflictError
from Exceptions.NotCleanWorkingTree import NotCleanWorkingTree
from FlexioFlow.StateHandler import StateHandler
from Branches.Branches import Branches
from Log.Log import Log
from VersionControl.Git.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.Git.GitCmd import GitCmd
from VersionControlProvider.Github.Message import Message
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic


class Finish:
    def __init__(self,
                 state_handler: StateHandler,
                 issue: Optional[Type[Issue]],
                 topic: Optional[Topic],
                 keep_branch: bool,
                 close_issue: bool
                 ):
        self.__state_handler: StateHandler = state_handler
        self.__issue: Optional[Type[Issue]] = issue
        self.__topic: Optional[Topic] = topic
        self.__git: GitCmd = GitCmd(self.__state_handler)
        self.__gitflow: GitFlowCmd = GitFlowCmd(self.__state_handler)
        self.__current_branch_name: str = self.__git.get_current_branch_name()
        self.__keep_branch: bool = keep_branch
        self.__close_issue: bool = close_issue

    def __init_gitflow(self) -> Finish:
        self.__gitflow.init_config()
        return self

    def __pull_develop(self) -> Finish:
        self.__git.checkout(Branches.DEVELOP).try_to_pull()
        return self

    def __merge_develop(self) -> Finish:
        self.__git.checkout_with_branch_name(self.__current_branch_name)

        message: Message = Message(
            message=''.join([
                "'Finish feature ` ",
                self.__current_branch_name,
                " ` for dev: ",
                self.__state_handler.version_as_str()
            ]),
            issue=self.__issue
        )

        message_str: str = ''
        if self.__close_issue:
            message_str = message.with_close()
        else:
            message_str = message.message

        self.__git.commit(
            message_str,
            ['--allow-empty']
        ).try_to_push()

        self.__git.checkout(Branches.DEVELOP).merge_with_version_message_from_branch_name(
            branch=self.__current_branch_name,
            message=Message(
                message='',
                issue=self.__issue
            ).with_ref(),
        ).try_to_push()

        if self.__git.has_conflict():
            raise GitMergeConflictError(Branches.DEVELOP.value, self.__git.get_conflict())
        return self

    def __delete_feature(self) -> Finish:
        if not self.__keep_branch:
            self.__git.delete_local_branch_from_name(self.__current_branch_name)
        self.__git.try_delete_remote_branch_from_name(self.__current_branch_name)
        return self

    def __finish_feature(self):
        self.__git.checkout_file_with_branch_name(Branches.DEVELOP.value, self.__state_handler.file_path())
        self.__merge_develop()
        if not self.__keep_branch:
            self.__delete_feature()

    def process(self):
        if not self.__git.is_clean_working_tree():
            raise NotCleanWorkingTree()
        if not self.__gitflow.is_feature():
            raise BranchNotExist(Branches.FEATURE.value)
        self.__pull_develop().__finish_feature()
