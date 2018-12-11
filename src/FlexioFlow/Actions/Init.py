from __future__ import annotations
from FlexioFlow.Version import Version
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from typing import List
from Exceptions.FileExistError import FileExistError
from FlexioFlow.Actions.Action import Action
from pathlib import Path
from VersionControl.VersionControl import VersionControl
from typing import Type
from FlexioFlow.Actions.Action import Action


class Init(Action):

    def __start_message(self) -> Init:
        print(
            """###############################################
################# Flexio FLow #################
###############################################
#################    Init     #################
""")
        return self

    def __input_version(self) -> Init:
        version: str = input('Version (0.0.0) : ')
        self.state_handler.state.version = Version.from_str(version if version else '0.0.0')
        return self

    def __input_level(self) -> Init:
        level: str = input('Level <(stable)|dev> : ')
        self.state_handler.state.level = Level[level.upper()] if level else Level.STABLE
        return self

    def __input_schemes(self) -> Init:
        schemes: List[Schemes] = []
        for scheme in Schemes:
            add: str = input('With ' + scheme.value + ' y/(n) : ')
            if add is 'y':
                schemes.append(scheme)

        self.state_handler.state.schemes = schemes
        return self

    def __write_file(self) -> Init:
        yml: str = self.state_handler.write_file()
        print("""#################################################
Write file : {0!s} 
#################################################""".format(self.state_handler.file_path()))
        print(yml)
        return self

    def __final_message(self) -> Init:
        print(
            """###############################################
Enjoy with Flexio FLow 
###############################################
""")
        return self

    def process(self):
        if self.state_handler.file_exists():
            raise FileExistError(self.state_handler.file_path(), 'Flexio Flow already initialized')

        self.__start_message() \
            .__input_version() \
            .__input_level() \
            .__input_schemes() \
            .__write_file() \
            .__final_message()
