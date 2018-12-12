from __future__ import annotations

from pathlib import Path
from subprocess import Popen
from typing import List


class GitFlowCmd:
    def __init__(self, dir_path: Path):
        self.__dir_path: Path = dir_path
        self.__branch: str = None

    def __exec(self, args: List[str]):
        Popen(args, cwd=self.__dir_path.as_posix()).communicate()

    def init_config(self) -> GitFlowCmd:
        self.__exec(["git", "flow", "init", "-f", "-d"])
        return self
