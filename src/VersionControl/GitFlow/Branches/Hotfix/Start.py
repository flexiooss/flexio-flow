from __future__ import annotations

from FlexioFlow.StateHandler import StateHandler
from VersionControl.Branches import Branches
from VersionControl.GitFlow.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.GitFlow.GitCmd import GitCmd


class Start:
    def __init__(self, state_handler: StateHandler):
        self.__state_handler: StateHandler = state_handler
        self.__git: GitCmd = GitCmd(self.__state_handler)
        self.__gitflow: GitFlowCmd = GitFlowCmd(self.__state_handler)

    def __init_gitflow(self) -> Start:
        self.__gitflow.init_config()
        return self

    def __pull_develop(self) -> Start:
        self.__git.checkout(Branches.DEVELOP).pull()
        return self

    def __pull_master(self) -> Start:
        self.__git.checkout(Branches.MASTER).pull()
        return self

    def __start_hotfix(self):
        GitFlowCmd(self.__state_handler).hotfix_start()

    def process(self):
        self.__init_gitflow().__pull_develop().__pull_master().__start_hotfix()
