from __future__ import annotations

import re
from subprocess import Popen, PIPE
from typing import List

from Exceptions.BranchAlreadyExist import BranchAlreadyExist
from Exceptions.BranchNotExist import BranchNotExist
from FlexioFlow.Level import Level
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.Version import Version
from Schemes.UpdateSchemeVersion import UpdateSchemeVersion
from VersionControl.BranchHandler import BranchHandler
from VersionControl.Branches import Branches
from VersionControl.GitFlow.GitCmd import GitCmd
from VersionControl.GitFlow.GitConfig import GitConfig


class GitFlowCmd:
    def __init__(self, state_handler: StateHandler):
        self.__state_handler: StateHandler = state_handler
        self.__branch: str = None
        self.__git: GitCmd = GitCmd(self.__state_handler)

    def __exec(self, args: List[str]):
        Popen(args, cwd=self.__state_handler.dir_path.as_posix()).communicate()

    def __exec_for_stdout(self, args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE, cwd=self.__state_handler.dir_path.as_posix()).communicate()
        return stdout.strip().decode('utf-8')

    def init_config(self) -> GitFlowCmd:
        self.__exec(["git", "flow", "init", "-f", "-d"])
        return self

    def hotfix_start(self) -> GitFlowCmd:
        if self.has_hotfix(True) or self.has_hotfix(False):
            raise BranchAlreadyExist(Branches.HOTFIX)

        self.__git.checkout(Branches.MASTER)
        next_version: Version = self.__state_handler.next_dev_patch()
        branch_name: str = BranchHandler.branch_name_from_version(Branches.HOTFIX, next_version)

        self.__git.create_branch_from(branch_name, Branches.MASTER)

        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)
        self.__git.commit(
            ''.join([
                "'Start hotfix : ",
                branch_name,
                "'"])
        ).set_upstream().push()
        return self

    def hotfix_finish(self) -> GitFlowCmd:
        if not self.has_hotfix(False):
            raise BranchNotExist(Branches.HOTFIX)

        self.__git.checkout(Branches.HOTFIX)
        self.__state_handler.set_stable()
        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)
        self.__git.commit(''.join(["'Finish hotfix for master: ", self.__state_handler.version_as_str()])).push()

        self.__git.checkout(Branches.MASTER).merge(Branches.HOTFIX).push().tag(
            self.__state_handler.version_as_str(),
            ' '.join([
                "'From Finished hotfix : ",
                self.__git.get_branch_name_from_git(Branches.HOTFIX),
                'tag : ',
                self.__state_handler.version_as_str(),
                "'"])
        ).push_tag(self.__state_handler.version_as_str())

        # self.__git.checkout(Branches.HOTFIX)
        #
        self.__git.checkout(Branches.DEVELOP).merge_file_with_ours(Branches.MASTER)
        self.__state_handler.next_dev_minor()
        self.__state_handler.set_dev()
        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)
        self.__git.commit(''.join(["'Finish hotfix for dev: ", self.__state_handler.version_as_str()])).push()

        self.__git.delete_branch(Branches.HOTFIX, True)
        self.__git.delete_branch(Branches.HOTFIX, False)
        return self

    def has_hotfix(self, remote: bool) -> bool:
        return self.__has_branch_from_parent(Branches.HOTFIX, remote)

    def has_release(self, remote: bool) -> bool:
        return self.__has_branch_from_parent(Branches.RELEASE, remote)

    def __has_branch_from_parent(self, branch: Branches, remote: bool) -> bool:
        if remote:
            resp: str = self.__exec_for_stdout(
                ['git', 'ls-remote', GitConfig.REMOTE.value, '"refs/heads/' + branch.value + '/*"'])
            return len(resp) > 0 and re.match(
                re.compile('.*refs/heads/' + branch.value + '/.*$'),
                resp
            ) is not None
        else:
            resp: str = self.__git.get_branch_name_from_git(branch)
            return len(resp) > 0
