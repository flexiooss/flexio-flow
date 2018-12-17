from __future__ import annotations
from FlexioFlow.StateHandler import StateHandler
from Schemes.UpdateSchemeVersion import UpdateSchemeVersion
from VersionControl.Branches import Branches
from VersionControl.GitFlow.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.GitFlow.GitCmd import GitCmd


class Finish:
    def __init__(self, state_handler: StateHandler):
        self.__state_handler: StateHandler = state_handler
        self.__git: GitCmd = GitCmd(self.__state_handler)
        self.__gitflow: GitFlowCmd = GitFlowCmd(self.__state_handler)

    def __init_gitflow(self) -> Finish:
        self.__gitflow.init_config()
        return self

    def __pull_develop(self) -> Finish:
        self.__git.checkout(Branches.DEVELOP).pull()
        return self

    def __pull_master(self) -> Finish:
        self.__git.checkout(Branches.MASTER).pull()
        return self

    def __finish_hotfix(self):
        print('__finish_hotfix')

        self.__gitflow.hotfix_finish()

    def process(self):
        self.__init_gitflow().__pull_develop().__pull_master().__finish_hotfix()
