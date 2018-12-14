from __future__ import annotations
from pathlib import Path
from subprocess import Popen
from typing import List

from FlexioFlow.Level import Level
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.Version import Version


class GitFlowCmd:
    def __init__(self, state_handler: StateHandler):
        self.__state_handler: StateHandler = state_handler
        self.__branch: str = None

    def __exec(self, args: List[str]):
        Popen(args, cwd=self.__state_handler.dir_path.as_posix()).communicate()

    def init_config(self) -> GitFlowCmd:
        self.__exec(["git", "flow", "init", "-f", "-d"])
        return self

    def hotfix_start(self) -> GitFlowCmd:
        next_version: Version = self.__state_handler.next_dev_patch()
        self.__exec(["git", "flow", "hotfix", "start", '-'.join([str(next_version), Level.DEV.value])])
        return self
