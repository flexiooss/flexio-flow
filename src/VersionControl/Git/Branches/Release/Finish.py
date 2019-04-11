from __future__ import annotations

from typing import Type, Optional

from Exceptions.BranchHaveDiverged import BranchHaveDiverged
from Exceptions.BranchNotExist import BranchNotExist
from Exceptions.GitMergeConflictError import GitMergeConflictError
from Exceptions.NotCleanWorkingTree import NotCleanWorkingTree
from Exceptions.RemoteDivergence import RemoteDivergence
from FlexioFlow.StateHandler import StateHandler
from Schemes.UpdateSchemeVersion import UpdateSchemeVersion
from Branches.Branches import Branches
from VersionControl.Git.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.Git.GitCmd import GitCmd
from VersionControlProvider.Github.Message import Message
from VersionControlProvider.Issue import Issue


class Finish:
    def __init__(self, state_handler: StateHandler, issue: Optional[Type[Issue]], keep_branch: bool):
        self.__state_handler: StateHandler = state_handler
        self.__issue: Optional[Type[Issue]] = issue
        self.__git: GitCmd = GitCmd(self.__state_handler)
        self.__gitflow: GitFlowCmd = GitFlowCmd(self.__state_handler)
        self.__keep_branch: bool = keep_branch
        self.__name: str = self.__git.get_branch_name_from_git(Branches.RELEASE)

    def __init_gitflow(self) -> Finish:
        self.__gitflow.init_config()
        return self

    def __pull_develop(self) -> Finish:
        if self.__git.has_remote() and not self.is_local_remote_equal(Branches.DEVELOP.value):
            raise RemoteDivergence(Branches.DEVELOP.value + 'should be merged with remote')
        # self.__git.checkout(Branches.DEVELOP).try_to_pull()
        return self

    def __pull_master(self) -> Finish:
        if self.__git.has_remote() and not self.is_local_remote_equal(Branches.MASTER.value):
            raise RemoteDivergence(Branches.MASTER.value + 'should be merged with remote')
        # self.__git.checkout(Branches.MASTER).try_to_pull()
        return self

    def __merge_master(self) -> Finish:
        self.__git.checkout(Branches.MASTER).merge_with_version_message(
            branch=Branches.RELEASE,
            message=Message(
                message='',
                issue=self.__issue
            ).with_ref(),
            options=['--no-ff', '--strategy-option', 'theirs']
        )

        if self.__git.has_conflict():
            raise GitMergeConflictError(Branches.MASTER.value, self.__git.get_conflict())

        self.__git.tag(
            self.__state_handler.version_as_str(),
            ' '.join([
                "'From Finished release : ",
                self.__git.get_branch_name_from_git(Branches.RELEASE),
                'tag : ',
                self.__state_handler.version_as_str(),
                "'"])
        ).try_to_push_tag(self.__state_handler.version_as_str()).try_to_push()

        return self

    def __merge_develop(self) -> Finish:
        self.__git.checkout_with_branch_name(self.__git.get_branch_name_from_git(Branches.RELEASE))
        self.__state_handler.next_dev_minor()
        self.__state_handler.set_dev()
        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)
        self.__git.commit(
            Message(
                message=''.join(["'Finish release for dev: ", self.__state_handler.version_as_str()]),
                issue=self.__issue
            ).with_ref()
        ).try_to_push()

        self.__git.checkout(Branches.DEVELOP).merge_with_version_message(
            branch=Branches.RELEASE,
            message=Message(
                message='',
                issue=self.__issue
            ).with_ref()
        )

        if self.__git.has_conflict():
            raise GitMergeConflictError(Branches.DEVELOP.value, self.__git.get_conflict())

        self.__git.try_to_push()

        return self

    def __delete_release(self) -> Finish:
        self.__git.delete_branch(Branches.RELEASE, True)
        self.__git.delete_branch(Branches.RELEASE, False)
        return self

    def __finish_release(self):
        if not self.__gitflow.has_release(False):
            raise BranchNotExist(Branches.RELEASE.value)
        self.__merge_master().__merge_develop()

        if not self.__keep_branch:
            self.__delete_release()

    def process(self):
        if not self.__git.is_clean_working_tree():
            raise NotCleanWorkingTree()

        if self.__git.is_branch_ahead(Branches.MASTER.value, self.__name):
            print(self.__git.list_commit_diff(Branches.MASTER.value, self.__name))
            raise BranchHaveDiverged('Oups !!! Master have commit ahead ' + self.__name + ' merge before')

        self.__pull_develop().__pull_master().__finish_release()
