from __future__ import annotations

import re
from subprocess import Popen, PIPE
from typing import List

from Exceptions.BranchNotExist import BranchNotExist
from FlexioFlow.StateHandler import StateHandler
from Branches.Branches import Branches
from Log.Log import Log
from VersionControl.Git.GitCmd import GitCmd
from VersionControl.Git.GitConfig import GitConfig
from Core.ConfigHandler import ConfigHandler
from ConsoleColors.Fg import Fg


class GitFlowCmd:
    def __init__(self, state_handler: StateHandler, config_handler: ConfigHandler):
        self.__state_handler: StateHandler = state_handler
        self.__config_handler: ConfigHandler = config_handler
        self.__branch: str = None
        self.__git: GitCmd = GitCmd(self.__state_handler).with_config_handler(config_handler)

    def __exec(self, args: List[str]):
        Popen(args, cwd=self.__state_handler.dir_path.as_posix()).communicate()

    def __exec_for_stdout(self, args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE, cwd=self.__state_handler.dir_path.as_posix()).communicate()
        return stdout.strip().decode('utf-8')

    def init_config(self) -> GitFlowCmd:
        return self.ensure_head().ensure_master_branch().ensure_develop_branch()

    def ensure_head(self) -> GitFlowCmd:
        if not self.__git.has_head():
            Log.warning('The repository does not have a HEAD yet')
            self.__git.init_head().commit('Initial commit', ['--allow-empty'])
            Log.info('Initial commit')
        return self

    def ensure_master_branch(self) -> GitFlowCmd:
        Log.info('Ensure have Master branch : ' + self.__config_handler.master())
        if not self.__git.local_branch_exists(self.__config_handler.master()):
            if not self.__git.remote_branch_exists(self.__config_handler.master()):
                Log.warning(self.__config_handler.master() + ' not exists')
                create: str = input(
                    'Create ' + self.__config_handler.master() + ' from current branch ?  y/' + Fg.SUCCESS.value + 'n' + Fg.RESET.value + ' : ')
                if create == 'y':
                    self.__git.create_branch_from(
                        self.__config_handler.master(),
                        self.__git.get_current_branch_name()
                    ).try_to_set_upstream().try_to_push()
                    self.ensure_master_branch()
                else:
                    raise BranchNotExist(self.__config_handler.master())
            else:
                Log.error('Remote branch : ' + self.__config_handler.master() + ' already exists, pull before')
        return self

    def ensure_develop_branch(self) -> GitFlowCmd:
        Log.info('Ensure have Develop branch : ' + self.__config_handler.develop())
        if not self.__git.branch_exists(self.__config_handler.develop()):
            self.__git.checkout(self.__config_handler.master()).create_branch_from(
                self.__config_handler.develop(),
                self.__config_handler.master()
            ).try_to_set_upstream().try_to_push()
        return self

    def has_hotfix(self, remote: bool) -> bool:
        return self.__has_branch_from_parent(self.__config_handler.hotfix(), remote)

    def has_release(self, remote: bool) -> bool:
        return self.__has_branch_from_parent(self.__config_handler.release(), remote)

    def has_feature(self, remote: bool) -> bool:
        return self.__has_branch_from_parent(self.__config_handler.feature(), remote)

    def is_feature(self) -> bool:
        resp: str = self.__git.get_current_branch_name()

        return len(resp) > 0 and re.match(
            re.compile('^' + self.__config_handler.feature() + '/.*$'),
            resp
        ) is not None

    def is_release(self) -> bool:
        resp: str = self.__git.get_current_branch_name()

        return len(resp) > 0 and re.match(
            re.compile('^' + self.__config_handler.release() + '/.*$'),
            resp
        ) is not None

    def is_hotfix(self) -> bool:
        resp: str = self.__git.get_current_branch_name()

        return len(resp) > 0 and re.match(
            re.compile('^' + self.__config_handler.hotfix() + '/.*$'),
            resp
        ) is not None

    def __has_branch_from_parent(self, branch: str, remote: bool) -> bool:
        if remote:
            resp: str = self.__exec_for_stdout(
                ['git', 'ls-remote', GitConfig.REMOTE.value, '"refs/heads/' + branch + '/*"'])
            return len(resp) > 0 and re.match(
                re.compile('.*refs/heads/' + branch + '/.*$'),
                resp
            ) is not None
        else:
            resp: str = self.__git.get_branch_name_from_git(branch)
            return len(resp) > 0
