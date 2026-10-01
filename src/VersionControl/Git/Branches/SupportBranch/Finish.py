from __future__ import annotations

from typing import Type, Optional, List

from Core.ConfigHandler import ConfigHandler
from Exceptions.GitMergeConflictError import GitMergeConflictError
from Exceptions.MergeCommitBetweenBounds import MergeCommitBetweenBounds
from Exceptions.NoBranchSelected import NoBranchSelected
from Exceptions.NoChangesInBranch import NoChangesInBranch
from Exceptions.NotCleanWorkingTree import NotCleanWorkingTree
from FlexioFlow.Options import Options
from FlexioFlow.StateHandler import StateHandler
from Schemes.UpdateSchemeVersion import UpdateSchemeVersion
from VersionControl.Git.GitCmd import GitCmd
from VersionControlProvider.Github.Message import Message
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic


class Finish:
    def __init__(self,
                 state_handler: StateHandler,
                 config_handler: ConfigHandler,
                 issue: Optional[Type[Issue]],
                 topics: Optional[List[Topic]],
                 keep_branch: bool,
                 close_issue: bool,
                 options: Options
                 ):
        self.__state_handler: StateHandler = state_handler
        self.__config_handler: ConfigHandler = config_handler
        self.__issue: Optional[Type[Issue]] = issue
        self.__topics: Optional[List[Topic]] = topics
        self.__keep_branch: bool = keep_branch
        self.__close_issue: bool = close_issue
        self.__options: Options = options
        self.__git: GitCmd = GitCmd(self.__state_handler).with_config_handler(config_handler)
        self.__current_branch_name: str = self.__git.get_current_branch_name()

    def __ensure_choice(self) -> bool:
        if self.__options.merge is not None:
            return self.__options.merge

        print("""
This fix was born on an older line. If the code changed on {0!s}, it may not
make sense there. The support branch is deleted at the end : a later report
would have to be done by hand, from the tag.
""".format(self.__config_handler.develop()))

        answer: str = input(' Report the fix to ' + self.__config_handler.develop() + ' Y/N : ')
        return answer.capitalize() == 'Y'

    def __low_bound(self) -> str:
        base: str = self.__git.merge_base(self.__current_branch_name, self.__config_handler.develop())
        return self.__git.first_commit_after(base, self.__current_branch_name)

    def __ensure_has_fix(self, low: str) -> None:
        if low == '' or self.__git.rev_parse(self.__current_branch_name) == low:
            raise NoChangesInBranch(self.__current_branch_name)

    def __close_line(self) -> str:
        self.__state_handler.set_stable()
        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)
        version: str = self.__state_handler.version_as_str()

        message: Message = Message(
            message='Finish support : ' + version,
            issue=self.__issue
        )
        self.__git.commit(message.with_close() if self.__close_issue else message.message).try_to_push()
        self.__git.tag(version, 'From finished support : ' + self.__current_branch_name)
        self.__git.try_to_push_tag(version)
        return version

    def __synthetic_message(self, version: str, low: str, high: str) -> str:
        return 'support ' + version + ' : report\n\nFrom support line, tag ' + version \
               + '\nOrigin commits :\n' + self.__git.log_oneline_between(low, high)

    def __merge_develop(self, version: str, low: str) -> None:
        high: str = self.__git.rev_parse(self.__current_branch_name + '~1')
        message: str = self.__synthetic_message(version, low, high)
        synthetic: str = self.__git.commit_tree(self.__git.tree_of(high), low, message)

        self.__git.checkout(self.__config_handler.develop()).try_to_pull()
        self.__git.cherry_pick_no_commit(synthetic)

        if self.__git.has_conflict():
            conflict: str = self.__git.get_conflict()
            if self.__options.default or self.__options.no_cli:
                self.__git.cherry_pick_abort()
            raise GitMergeConflictError(self.__config_handler.develop(), conflict)

        self.__git.commit(message).try_to_push()

    def __delete_branch(self) -> None:
        self.__git.checkout(self.__config_handler.develop())
        if self.__git.has_remote():
            self.__git.delete_remote_branch_from_name(self.__current_branch_name)
        self.__git.delete_local_branch_from_name(self.__current_branch_name)

    def process(self):
        if not self.__config_handler.config.branches_config.is_support(
                self.__current_branch_name.split('/')[0]):
            raise NoBranchSelected('Checkout to a support branch before')
        if not self.__git.is_clean_working_tree():
            raise NotCleanWorkingTree()

        merge: bool = self.__ensure_choice()
        low: str = self.__low_bound()
        self.__ensure_has_fix(low)

        if merge and self.__git.has_merge_commit_between(low, self.__current_branch_name):
            raise MergeCommitBetweenBounds(self.__current_branch_name)

        version: str = self.__close_line()

        if merge:
            self.__merge_develop(version, low)

        if not self.__keep_branch:
            self.__delete_branch()
