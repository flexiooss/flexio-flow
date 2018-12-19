from __future__ import annotations

from Exceptions.BranchAlreadyExist import BranchAlreadyExist
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.Version import Version
from Schemes.UpdateSchemeVersion import UpdateSchemeVersion
from VersionControl.BranchHandler import BranchHandler
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
        if self.__gitflow.has_release(True) or self.__gitflow.has_release(False):
            raise BranchAlreadyExist(Branches.RELEASE)
        if self.__gitflow.has_hotfix(True) or self.__gitflow.has_hotfix(False):
            raise BranchAlreadyExist(Branches.HOTFIX)

        self.__git.checkout(Branches.MASTER)
        next_version: Version = self.__state_handler.next_dev_patch()
        branch_name: str = BranchHandler.branch_name_from_version(Branches.HOTFIX, next_version)

        self.__git.create_branch_from(branch_name, Branches.MASTER)

        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)
        self.__git.commit(
            "'Start hotfix : {branch_name!s}'".format(branch_name=branch_name)
        ).set_upstream()

    def process(self):
        self.__init_gitflow().__pull_develop().__pull_master().__start_hotfix()
