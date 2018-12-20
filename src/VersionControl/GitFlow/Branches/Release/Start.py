from __future__ import annotations

from Exceptions.BranchAlreadyExist import BranchAlreadyExist
from FlexioFlow.StateHandler import StateHandler
from Schemes.UpdateSchemeVersion import UpdateSchemeVersion
from Branches.BranchHandler import BranchHandler
from Branches.Branches import Branches
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

    def __start_release(self):
        if self.__gitflow.has_release(True) or self.__gitflow.has_release(False):
            raise BranchAlreadyExist(Branches.RELEASE)
        if self.__gitflow.has_hotfix(True) or self.__gitflow.has_hotfix(False):
            raise BranchAlreadyExist(Branches.HOTFIX)

        self.__git.checkout(Branches.DEVELOP)
        branch_name: str = BranchHandler.branch_name_from_version(
            Branches.RELEASE,
            self.__state_handler.state.version
        )

        self.__git.create_branch_from(branch_name, Branches.DEVELOP)

        self.__state_handler.set_stable()
        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)

        self.__git.commit(
            ''.join([
                "'Start release : ",
                branch_name,
                "'"])
        ).set_upstream()

    def process(self):
        self.__init_gitflow().__pull_develop().__pull_master().__start_release()
