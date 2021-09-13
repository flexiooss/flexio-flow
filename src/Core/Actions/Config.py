from __future__ import annotations

from subprocess import Popen, PIPE
from typing import List

from Core.Actions.InputBranchesConfig import InputBranchesConfig
from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Flexio.InputConfig import InputConfig as FlexioInputConfig
from VersionControlProvider.Github.InputConfig import InputConfig as GithubInputConfig
from Core.Config import Config as FFConfig

from VersionControlProvider.Flexio.ConfigFlexio import ConfigFlexio
from VersionControlProvider.Github.ConfigGithub import ConfigGithub
from Branches.BranchesConfig import BranchesConfig
from Branches.Branches import Branches

class Config:
    def __init__(self, config_handler: ConfigHandler):
        self.config_handler: ConfigHandler = config_handler

    def __config_handler(self) -> ConfigHandler:
        return self.config_handler

    def __exec(self, args: List[str]):
        Popen(args, cwd=self.config_handler.dir_path.as_posix()).communicate()

    def __exec_for_stdout(self, args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE, cwd=self.config_handler.dir_path.as_posix()).communicate()
        return stdout.strip().decode('utf-8')

    def __start_message(self) -> Config:
        print(
            """#######################################################################################
#######################################################################################
#######################################################################################

   __  _            _             __  _
  / _|| | ___ __ __(_) ___  ___  / _|| | ___ __ __ __
 |  _|| |/ -_)\ \ /| |/ _ \|___||  _|| |/ _ \\ V  V /
 |_|  |_|\___|/_\_\|_|\___/     |_|  |_|\___/ \_/\_/

https://github.com/flexiooss/flexio-flow

#################################################
#################    Config     #################
#################################################
""")
        return self

    def __write_file(self) -> Config:
        yml: str = self.__config_handler().write_file()

        print(yml)
        return self

    def __final_message(self) -> Config:
        print(
            """###############################################
Enjoy with Flexio FLow 
###############################################
""")
        return self

    def __default_config(self):
        self.config_handler.config = FFConfig().with_github(
            github=ConfigGithub(
                activate=False,
                user='',
                token=''
            )
        ).with_flexio(flexio=ConfigFlexio(
            activate=False,
            user_token=''
        )).with_branches_config(branches_config=BranchesConfig.from_dict(
            {Branches.MASTER.value: Branches.MASTER.value, Branches.DEVELOP.value: Branches.DEVELOP.value,
             Branches.FEATURE.value: Branches.FEATURE.value, Branches.HOTFIX.value: Branches.HOTFIX.value,
             Branches.RELEASE.value: Branches.RELEASE.value}))

    def __ensure_have_config(self) -> Config:
        if self.__config_handler().file_exists():
            self.__config_handler().load_file_config()
            print(
                """###############################################
Flexio Flow  
Core already initialized at : {path!s}
###############################################

{config!s}

""".format(
                    path=self.__config_handler().file_path().as_posix(),
                    config=str(self.__config_handler().config.to_dict())
                )

            )

            change: str = input('Change this file y/(n) : ')
            change = change if change else 'n'
            if change == 'n':
                return self
        else:
            self.config_handler.reset_config()
            self.__default_config()

        if not self.config_handler.dir_path.exists():
            self.config_handler.dir_path.mkdir()

        self.__start_message()
        InputBranchesConfig(self.config_handler).add_to_config_handler()
        GithubInputConfig(self.config_handler).add_to_config_handler()
        FlexioInputConfig(self.config_handler).add_to_config_handler()

        self.__write_file()

        return self

    def process(self):
        self.__ensure_have_config()
        self.__final_message()
