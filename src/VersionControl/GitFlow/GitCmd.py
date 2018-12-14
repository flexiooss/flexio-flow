from __future__ import annotations

import re
from pathlib import Path
from subprocess import Popen, PIPE
from typing import List, Optional

from Exceptions.FileNotExistError import FileNotExistError
from Exceptions.NoBranchSelected import NoBranchSelected
from FlexioFlow.Level import Level
from FlexioFlow.StateHandler import StateHandler
from VersionControl.Branches import Branches
from VersionControl.GitFlow.GitConfig import GitConfig


class GitCmd:
    def __init__(self, state_handler: StateHandler):
        self.__state_handler = state_handler
        self.__branch: Optional[Branches] = None
        self.__remote_branch_name: Optional[str] = None

    def __exec(self, args: List[str]):
        Popen(args, cwd=self.__state_handler.dir_path.as_posix()).communicate()

    def __exec_for_stdout(self, args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE, cwd=self.__state_handler.dir_path.as_posix()).communicate()
        return stdout.strip().decode('utf-8')

    def add_all(self) -> GitCmd:
        self.__exec(['git', 'add', '.'])
        return self

    def branch_exists(self, branch: str, remote: bool) -> bool:
        if remote:
            resp: str = self.__exec_for_stdout(['git', 'ls-remote', GitConfig.REMOTE.value, 'refs/heads/' + branch])
            return len(resp) > 0 and re.match(re.compile('.*refs/heads/' + branch + '$'), resp) is not None
        else:
            resp: str = self.__exec_for_stdout(['git', 'branch', '-l', '|', 'grep', branch])
            return len(resp) > 0 and re.match(re.compile(branch + '$'), resp) is not None

    def checkout(self, branch: Branches) -> GitCmd:
        self.__branch = branch
        self.__ensure_remote_branch_name()
        self.__exec(['git', 'checkout', self.__remote_branch_name])
        try:
            self.__state_handler.load_file_config()
        except FileNotExistError as e:
            print(e)
        return self

    def __ensure_remote_branch_name(self) -> GitCmd:
        if not self.__branch:
            raise NoBranchSelected('Try with GitCmd.checkout(branch_name:str) before')
        branch_name: str = self.__branch.value
        if self.__branch in [Branches.HOTFIX, Branches.RELEASE]:
            self.__exec(['git', 'checkout', Branches.MASTER.value])
            self.__state_handler.load_file_config()
            name: str = str(self.__state_handler.next_dev_patch())
            name = (name + '-' + Level.DEV.value) if self.__branch is Branches.HOTFIX else name
            branch_name = '/'.join([self.__branch.value, name])
        self.__remote_branch_name = branch_name
        return self

    def clone(self, url: str) -> GitCmd:
        self.__exec(['git', 'clone', url, '.'])
        return self

    def get_current_branch_name(self) -> str:
        # return self.__exec_for_stdout(['git', 'branch', '|', 'grep', '\*', '|', 'cut', '-d', '" "', '-f2'])
        return self.__exec_for_stdout(['git', 'symbolic-ref', '--short', 'HEAD'])

    def commit(self, msg: str) -> GitCmd:
        self.__exec(["git", "commit", "-am", msg])
        return self

    def delete_tag(self, tag: str, remote: bool) -> GitCmd:
        if remote:
            self.__exec(['git', 'push', GitConfig.REMOTE.value, '--delete', tag])
        else:
            self.__exec(['git', 'tag', '-d', tag])
        return self

    def delete_branch(self, branch: str, remote: bool) -> GitCmd:
        if remote:
            self.__exec(['git', 'push', GitConfig.REMOTE.value, '--delete', branch])
        else:
            self.__exec(['git', 'branch', '-d', branch])
        return self

    def last_tag(self) -> str:
        return self.__exec_for_stdout(['git', 'describe', '--abbrev=0', '--tags'])

    def push_tag(self, tag: str) -> GitCmd:
        self.__exec(["git", "push", GitConfig.REMOTE.value, tag])
        return self

    def pull(self) -> GitCmd:
        self.__exec(["git", "pull"])
        return self

    def push(self) -> GitCmd:
        self.__exec(["git", "push"])
        return self

    def push_force(self) -> GitCmd:
        if not self.__branch:
            raise NoBranchSelected('Try with GitCmd.checkout(branch_name:str) before')
        self.__exec(['git', 'push', '--force', GitConfig.REMOTE.value, self.get_current_branch_name()])
        # self.__exec(['git', 'push', '--force', GitConfig.REMOTE.value, self.__branch])
        return self

    def tag_exists(self, tag: str, remote: bool) -> bool:
        if remote:
            resp: str = self.__exec_for_stdout(['git', 'ls-remote', GitConfig.REMOTE.value, 'refs/tags/' + tag])
            return len(resp) > 0 and re.match(re.compile('.*refs/tags/' + tag + '$'), resp) is not None
        else:
            resp: str = self.__exec_for_stdout(['git', 'tag', '-l', '|', 'grep', tag])
            return len(resp) > 0 and re.match(re.compile('^' + tag + '$'), resp) is not None

    def reset_to_tag(self, tag: str) -> GitCmd:
        self.__exec(['git', 'reset', '--hard', tag])
        return self

    def set_upstream(self) -> GitCmd:
        if not self.__branch:
            raise NoBranchSelected('Try with GitCmd.checkout(branch_name:str) before')
        self.__exec(["git", "push", "--set-upstream", GitConfig.REMOTE.value, self.get_current_branch_name()])
        # self.__exec(["git", "push", "--set-upstream", GitConfig.REMOTE.value, self.__branch])
        return self

    def tag(self, tag: str, msg: Optional[str] = None) -> GitCmd:
        msg = msg if msg else tag
        self.__exec(["git", "tag", "-a", tag, "-m", "'" + msg + "'"])
        return self
