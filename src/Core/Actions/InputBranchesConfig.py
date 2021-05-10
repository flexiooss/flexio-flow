from Branches.BranchesConfig import BranchesConfig
from Branches.Branches import Branches
from Core.ConfigHandler import ConfigHandler
from ConsoleColors.Fg import Fg


class InputBranchesConfig:
    def __init__(self, config_handler: ConfigHandler):
        self.config_handler: ConfigHandler = config_handler

    def __input(self, branch: Branches, name: str) -> str:
        v: str = input(branch.value + ' branch name : ' + Fg.SUCCESS.value + name + Fg.RESET.value+' ')
        v = v if v else name
        return v

    def add_to_config_handler(self) -> ConfigHandler:
        master: str = self.__input(Branches.MASTER, self.config_handler.master())
        develop: str = self.__input(Branches.DEVELOP, self.config_handler.develop())
        feature: str = self.__input(Branches.FEATURE, self.config_handler.feature())
        hotfix: str = self.__input(Branches.HOTFIX, self.config_handler.hotfix())
        release: str = self.__input(Branches.RELEASE, self.config_handler.release())

        self.config_handler.config = self.config_handler.config.with_branches_config(
            BranchesConfig(develop, feature, hotfix, master, release))
        return self.config_handler
