from __future__ import annotations
from FlexioFlow.Version import Version
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from typing import List
from Branches.Actions.Action import Action
from Branches.Actions.Actions import Actions
from Branches.Branches import Branches


class Commit(Action):

    def __start_message(self) -> Commit:
        print(
            """###############################################
################# Flexio FLow #################
###############################################
#################    Commit     #################
""")
        return self

    def __input_version(self) -> Commit:
        version: str = input('Version (0.0.0) : ')
        self.state_handler.state.version = Version.from_str(version if version else '0.0.0')
        return self

    def __input_level(self) -> Commit:
        level: str = input('Level <(stable)|dev> : ')
        self.state_handler.state.level = Level[level.upper()] if level else Level.STABLE
        return self

    def __input_schemes(self) -> Commit:
        schemes: List[Schemes] = []
        for scheme in Schemes:
            add: str = input('With ' + scheme.value + ' y/(n) : ')
            if add is 'y':
                schemes.append(scheme)

        self.state_handler.state.schemes = schemes
        return self

    def __write_file(self) -> Commit:
        yml: str = self.state_handler.write_file()
        print("""#################################################
Write file : {0!s} 
#################################################""".format(self.state_handler.file_path()))
        print(yml)
        return self

    def __final_message(self) -> Commit:
        print(
            """###############################################
Enjoy with Flexio FLow 
###############################################
""")
        return self

    def __ensure_have_state(self) -> bool:
        if self.state_handler.file_exists():
            self.state_handler.load_file_config()
            print(
                """###############################################
Flexio Flow already Commitialized 
###############################################
""")
            print('at : ' + self.state_handler.file_path().as_posix())
            print('with : ' + str(self.state_handler.state.to_dict()))
            use: str = input('Use this file (y)/n : ')
            use = use if use else 'y'
            if use is 'y':
                return True

        self.__start_message() \
            .__input_version() \
            .__input_level() \
            .__input_schemes()

        return False

    def __ensure_version_control_Commitialized(self):
        self.version_control.build_branch(Branches.MASTER).with_action(Actions.Commit).process()

    def process(self):
        if not self.__ensure_have_state():
            self.__ensure_version_control_Commitialized()

        self.__final_message()
