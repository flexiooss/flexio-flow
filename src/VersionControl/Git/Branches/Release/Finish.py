from __future__ import annotations

from typing import Type, Optional, List

from Exceptions.BranchHaveDiverged import BranchHaveDiverged
from Exceptions.BranchNotExist import BranchNotExist
from Exceptions.GitMergeConflictError import GitMergeConflictError
from Exceptions.NoBranchSelected import NoBranchSelected
from Exceptions.NotCleanWorkingTree import NotCleanWorkingTree
from Exceptions.RemoteDivergence import RemoteDivergence
from FlexioFlow.StateHandler import StateHandler
from Log.Log import Log
from Schemes.UpdateSchemeVersion import UpdateSchemeVersion
from Branches.Branches import Branches
from VersionControl.Git.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.Git.GitCmd import GitCmd
from VersionControlProvider.Github.Message import Message
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic
from ConsoleColors.Fg import Fg
from Core.ConfigHandler import ConfigHandler


class Finish:
    def __init__(self,
                 state_handler: StateHandler,
                 config_handler: ConfigHandler,
                 issue: Optional[Type[Issue]],
                 topics: Optional[List[Topic]],
                 keep_branch: bool,
                 close_issue: bool
                 ):
        self.__state_handler: StateHandler = state_handler
        self.__config_handler: ConfigHandler = config_handler
        self.__issue: Optional[Type[Issue]] = issue
        self.__topics: Optional[List[Topic]] = topics
        self.__git: GitCmd = GitCmd(self.__state_handler)
        self.__gitflow: GitFlowCmd = GitFlowCmd(self.__state_handler,config_handler)
        self.__keep_branch: bool = keep_branch
        self.__close_issue: bool = close_issue
        self.__name: str = self.__git.get_branch_name_from_git(config_handler.release())
        self.__version_check: str = self.__state_handler.version_as_str()

    def __init_gitflow(self) -> Finish:
        self.__gitflow.init_config()
        return self

    def __checkout_current_release(self):
        self.__git.checkout_with_branch_name(self.__name)

    def __pull_develop(self) -> Finish:
        # if self.__git.has_remote() and not self.__git.is_local_remote_equal(Branches.DEVELOP.value):
        #     raise RemoteDivergence(Branches.DEVELOP.value + 'should be merged with remote')
        self.__git.checkout(self.__config_handler.develop()).try_to_pull()
        return self

    def __pull_master(self) -> Finish:
        # if self.__git.has_remote() and not self.__git.is_local_remote_equal(Branches.MASTER.value):
        #     raise RemoteDivergence(Branches.MASTER.value + 'should be merged with remote')
        self.__git.checkout(self.__config_handler.master()).try_to_pull()
        return self

    def __merge_master(self) -> Finish:

        message: Message = Message(
            message='Merge ' + self.__name + 'into ' + self.__config_handler.master(),
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
        )

        self.__git.checkout(self.__config_handler.master()).merge_with_version_message(
            branch=self.__config_handler.release(),
            message=message_str,
            options=['--no-ff', '--strategy-option', 'theirs']
        )

        if self.__git.has_conflict():
            raise GitMergeConflictError(self.__config_handler.master(), self.__git.get_conflict())

        tag: str = self.__state_handler.version_as_str()

        if tag != self.__version_check:
            Log.error('Version have diverged during merge : ' + tag + 'should be ' + self.__version_check)
            raise GitMergeConflictError(self.__config_handler.master())

        self.__git.tag(
            tag,
            ' '.join([
                "'From Finished release : ",
                self.__name,
                'tag : ',
                tag,
                "'"])
        ).try_to_push_tag(tag).try_to_push()

        self.__git.checkout(self.__config_handler.release()).merge_with_version_message_from_branch_name(
            branch=tag,
            message=Message(
                message='Merge ' + tag + ' tag into ' + self.__name,
                issue=self.__issue
            ).with_ref(),
            options=['--no-ff']
        )

        return self

    def __merge_develop(self) -> Finish:
        self.__checkout_current_release()
        self.__state_handler.next_dev_minor()
        self.__state_handler.set_dev()
        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)

        self.__git.commit(
            Message(
                message=''.join(["'Finish release ready for dev next release : ", self.__state_handler.version_as_str()]),
                issue=self.__issue
            ).with_ref()
        )

        self.__git.checkout(self.__config_handler.develop()).merge_with_version_message(
            branch=self.__config_handler.release(),
            message=Message(
                message='',
                issue=self.__issue
            ).with_ref()
        )

        if self.__git.has_conflict():
            Log.error("""

{fg_fail}CONFLICT : resolve conflict, and remove your release branch manually{reset_fg}

            """.format(
                fg_fail=Fg.FAIL.value,
                reset_fg=Fg.RESET.value,
            ))
            raise GitMergeConflictError(self.__config_handler.develop(), self.__git.get_conflict())

        self.__git.checkout(self.__config_handler.release()).undo_last_commit()

        self.__git.checkout(self.__config_handler.develop()).try_to_push()

        return self

    def __delete_release(self) -> Finish:
        if not self.__keep_branch:
            self.__git.delete_local_branch_from_name(self.__name)
        self.__git.try_delete_remote_branch_from_name(self.__name)
        return self

    def __finish_release(self):
        if not self.__gitflow.has_release(False):
            raise BranchNotExist(self.__config_handler.release())
        self.__merge_master().__merge_develop()

        self.__delete_release()

    def process(self):
        if not self.__gitflow.is_release():
            raise NoBranchSelected('Checkout to release branch before')

        if not self.__git.is_clean_working_tree():
            raise NotCleanWorkingTree()

        self.__pull_master()

        if self.__git.is_branch_ahead(self.__config_handler.master(), self.__name):
            Log.error("""

            {fg_fail}{list}{reset_fg}

                        """.format(
                fg_fail=Fg.FAIL.value,
                list=self.__git.list_commit_diff(self.__config_handler.master(), self.__name),
                reset_fg=Fg.RESET.value,
            ))
            self.__checkout_current_release()

            raise BranchHaveDiverged(
                """
    
    {fg_fail}{message}{reset_fg}
    
                            """.format(
                    fg_fail=Fg.FAIL.value,
                    message='Oups !!! Master:'+self.__config_handler.master()+' have commit ahead ' + self.__name + ' merge before',
                    reset_fg=Fg.RESET.value,
                )
            )

        self.__pull_develop().__finish_release()
