from __future__ import annotations

from Exceptions.NotCleanWorkingTree import NotCleanWorkingTree
from FlexioFlow.Level import Level
from FlexioFlow.StateHandler import StateHandler
from Log.Log import Log
from Schemes.UpdateSchemeVersion import UpdateSchemeVersion
from Branches.Branches import Branches
from VersionControl.Git.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.Git.GitCmd import GitCmd


class Init:
    def __init__(self, state_handler: StateHandler):
        self.__state_handler: StateHandler = state_handler
        self.__git: GitCmd = GitCmd(self.__state_handler)


    def __init_gitflow(self) -> Init:
        GitFlowCmd(self.__state_handler).init_config()
        return self

    def __init_develop(self) -> Init:
        version: str = '-'.join([str(self.__state_handler.state.version), Level.DEV.value])

        self.__git.checkout_without_refresh_state(Branches.DEVELOP)

        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)

        self.__git.add_all().commit(
            ''.join(["'Init develop : ", version, "'"])
        ).try_to_set_upstream()

        Log.info('Init develop at : ' + version)
        return self

    def process(self):
        if not self.__git.is_clean_working_tree():
            raise NotCleanWorkingTree()
        self.__init_gitflow().__init_develop()
