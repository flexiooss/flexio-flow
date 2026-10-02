from __future__ import annotations

from typing import Type, Optional, List

from Branches.BranchHandler import BranchHandler
from Core.ConfigHandler import ConfigHandler
from Exceptions.FromTagRequired import FromTagRequired
from Exceptions.NotCleanWorkingTree import NotCleanWorkingTree
from Exceptions.TagIsMasterTip import TagIsMasterTip
from Exceptions.TagNotFound import TagNotFound
from Exceptions.TagNotPushed import TagNotPushed
from Exceptions.TagVersionMismatch import TagVersionMismatch
from FlexioFlow.Options import Options
from FlexioFlow.StateHandler import StateHandler
from Schemes.UpdateSchemeVersion import UpdateSchemeVersion
from VersionControl.Git.GitCmd import GitCmd
from VersionControl.Git.GitConfig import GitConfig
from VersionControlProvider.Github.Message import Message
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic


class Start:
    def __init__(self,
                 state_handler: StateHandler,
                 config_handler: ConfigHandler,
                 issue: Optional[Type[Issue]],
                 topics: Optional[List[Topic]],
                 options: Options
                 ):
        self.__state_handler: StateHandler = state_handler
        self.__config_handler: ConfigHandler = config_handler
        self.__issue: Optional[Type[Issue]] = issue
        self.__topics: Optional[List[Topic]] = topics
        self.__options: Options = options
        self.__git: GitCmd = GitCmd(self.__state_handler).with_config_handler(config_handler)

    def __resolve_tag(self) -> str:
        if self.__options.from_tag is None:
            raise FromTagRequired()
        return self.__options.from_tag

    def __ensure_tag_usable(self, tag: str) -> None:
        local: bool = self.__git.local_tag_exists(tag)
        remote: bool = self.__git.remote_tag_exists(tag) if self.__git.has_remote() else local

        if not local and not remote:
            raise TagNotFound(tag, self.__git.all_tags())
        if local and not remote:
            raise TagNotPushed(tag)

    def __master_ref(self) -> str:
        if self.__git.has_remote():
            return GitConfig.REMOTE.value + '/' + self.__config_handler.master()
        return self.__config_handler.master()

    def __ensure_not_master_tip(self, tag: str) -> None:
        if self.__git.rev_parse(tag + '^{commit}') == self.__git.rev_parse(self.__master_ref()):
            raise TagIsMasterTip(tag)

    def __rollback(self, origin_branch: str, origin_revision: str, created_branch: str) -> None:
        if origin_branch:
            self.__git.checkout_with_branch_name(origin_branch)
        else:
            self.__git.checkout_with_branch_name(origin_revision)
        self.__git.delete_local_branch_from_name(created_branch)

    def __start_support(self, tag: str) -> None:
        origin_branch: str = self.__git.get_current_branch_name()
        origin_revision: str = self.__git.rev_parse('HEAD')
        created_branch: str = 'support-start-' + tag

        self.__git.create_branch_from_revision(created_branch, tag)

        try:
            self.__state_handler.load_file_config()

            if self.__state_handler.version_as_str() != tag:
                raise TagVersionMismatch(tag, self.__state_handler.version_as_str())

            branch_name: str = BranchHandler(
                self.__config_handler.support(),
                self.__config_handler.config.branches_config
            ).with_issue(self.__issue).with_topics(self.__topics).branch_name_from_version(
                self.__state_handler.state.version.next_support())

            self.__git.rename_current_branch(branch_name)
            created_branch = branch_name

            self.__state_handler.next_dev_support()
            self.__state_handler.write_file()
            UpdateSchemeVersion.from_state_handler(self.__state_handler)
            self.__git.commit(
                Message(
                    message='Start support : ' + branch_name,
                    issue=self.__issue
                ).with_ref()
            ).try_to_set_upstream()
        except Exception:
            self.__rollback(origin_branch, origin_revision, created_branch)
            raise

    def process(self):
        if not self.__git.is_clean_working_tree():
            raise NotCleanWorkingTree()
        self.__git.try_to_fetch_tags()
        tag: str = self.__resolve_tag()
        self.__ensure_tag_usable(tag)
        self.__ensure_not_master_tip(tag)
        self.__start_support(tag)
