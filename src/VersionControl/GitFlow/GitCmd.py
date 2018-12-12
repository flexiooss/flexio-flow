from __future__ import annotations
from pathlib import Path
from subprocess import Popen, PIPE
from typing import List

from VersionControl.GitFlow.GitFlow import GitFlow


class GitCmd:
    def __init__(self, dir_path: Path):
        self.__dir_path: Path = dir_path

    def __exec(self, args: List[str]):
        Popen(args, cwd=self.__dir_path.as_posix()).communicate()

    def checkout(self, branch_name: str) -> GitCmd:
        self.__exec([
            'git',
            'checkout',
            branch_name
        ])
        return self

    def remote_tag_exists(self, tag: str, dir_path: Path) -> bool:
        stdout, stderr = Popen([
            'git',
            'ls-remote',
            GitFlow.REMOTE,
            'refs/tags/' + tag
        ], stdout=PIPE, cwd=self.__dir_path.as_posix()).communicate()
        print(stdout.strip())
        return len(stdout.strip()) > 0

    def delete_tag(self, tag: str) -> GitCmd:
        self.__exec(['git', 'push', GitFlow.REMOTE, '--delete', tag
                     ])
        return self

    def add_all_files(self) -> GitCmd:
        self.__exec(['git', 'add', '.'])
        return self

    def push_tag(self, tag: str) -> GitCmd:
        self.__exec(["git", "push", GitFlow.REMOTE, tag])
        return self
