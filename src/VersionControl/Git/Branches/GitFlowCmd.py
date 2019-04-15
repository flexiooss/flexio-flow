from __future__ import annotations

import re
from subprocess import Popen, PIPE
from typing import List
from FlexioFlow.StateHandler import StateHandler
from Branches.Branches import Branches
from Log.Log import Log
from VersionControl.Git.GitCmd import GitCmd
from VersionControl.Git.GitConfig import GitConfig


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
        return self.ensure_head().ensure_master_branch().ensure_develop_branch()

    def ensure_head(self) -> GitFlowCmd:
        if not self.__git.has_head():
            print('The repository does not have a HEAD yet')
            self.__git.init_head().commit('Initial commit', ['--allow-empty'])
        return self

    def ensure_master_branch(self) -> GitFlowCmd:
        Log.info('Ensure have Master branch')
        if not self.__git.local_branch_exists(Branches.MASTER.value):
            self.ensure_head()
        return self

    def ensure_develop_branch(self) -> GitFlowCmd:
        Log.info('Ensure have Develop branch')
        if not self.__git.branch_exists(Branches.DEVELOP.value):
            self.__git.checkout(Branches.MASTER).create_branch_from(
                Branches.DEVELOP.value,
                Branches.MASTER
            ).try_to_set_upstream().try_to_push()
        return self

    def has_hotfix(self, remote: bool) -> bool:
        return self.__has_branch_from_parent(Branches.HOTFIX, remote)

    def has_release(self, remote: bool) -> bool:
        return self.__has_branch_from_parent(Branches.RELEASE, remote)

    def has_feature(self, remote: bool) -> bool:
        return self.__has_branch_from_parent(Branches.FEATURE, remote)

    def is_feature(self) -> bool:
        resp: str = self.__git.get_current_branch_name()

        return len(resp) > 0 and re.match(
            re.compile('^' + Branches.FEATURE.value + '/.*$'),
            resp
        ) is not None

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
