from __future__ import annotations
from pathlib import Path
from subprocess import Popen, PIPE
from typing import List, Optional
from Exceptions.NoBranchSelected import NoBranchSelected
from VersionControl.GitFlow.GitConfig import GitConfig


class GitCmd:
    def __init__(self, dir_path: Path):
        self.__dir_path: Path = dir_path
        self.__branch: str = None

    def __exec(self, args: List[str]):
        Popen(args, cwd=self.__dir_path.as_posix()).communicate()

    def add_all(self) -> GitCmd:
        self.__exec(['git', 'add', '.'])
        return self

    def add_tag(self, tag: str, msg: Optional[str] = None) -> GitCmd:
        msg = msg if msg else tag
        self.__exec(["git", "tag", "-a", tag, "-m",
                     "'" + msg + "'"])
        return self

    def checkout(self, branch_name: str) -> GitCmd:
        self.__branch = branch_name
        self.__exec([
            'git',
            'checkout',
            branch_name
        ])
        return self

    def clone(self, url: str) -> GitCmd:
        self.__exec(['git', 'clone', url, '.'])
        return self

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
        stdout, stderr = Popen([
            'git',
            'describe',
            '--abbrev=0',
            '--tags'
        ], stdout=PIPE, cwd=self.__dir_path.as_posix()).communicate()
        return stdout.strip()

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

        self.__exec(['git', 'push', '--force', GitConfig.REMOTE.value, self.__branch])
        return self

    def remote_tag_exists(self, tag: str) -> bool:
        stdout, stderr = Popen([
            'git',
            'ls-remote',
            GitConfig.REMOTE.value,
            'refs/tags/' + tag
        ], stdout=PIPE, cwd=self.__dir_path.as_posix()).communicate()
        print(stdout.strip())
        return len(stdout.strip()) > 0

    def reset_to_tag(self, tag: str) -> GitCmd:
        self.__exec(['git', 'reset', '--hard', tag])
        return self

    def set_upstream(self) -> GitCmd:
        if not self.__branch:
            raise NoBranchSelected('Try with GitCmd.checkout(branch_name:str) before')
        self.__exec(["git", "push", "--set-upstream", GitConfig.REMOTE.value, self.__branch])
        return self
