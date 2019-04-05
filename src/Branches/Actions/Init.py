from __future__ import annotations
from FlexioFlow.Version import Version
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from typing import List
from Branches.Actions.Action import Action
from Branches.Actions.Actions import Actions
from Branches.Branches import Branches
from ConsoleColors.Fg import Fg
from ConsoleColors.PrintColor import PrintColor


class Init(Action):

    def __start_message(self) -> Init:
        print(
            """######################################################{fg_yellow}
   __  _            _             __  _
  / _|| | ___ __ __(_) ___  ___  / _|| | ___ __ __ __
 |  _|| |/ -_)\ \ /| |/ _ \|___||  _|| |/ _ \\ V  V /
 |_|  |_|\___|/_\_\|_|\___/     |_|  |_|\___/ \_/\_/

{reset_fg}######################################################
#####################    {fg_yellow}Init{reset_fg}     ####################
""".format(

                fg_yellow=Fg.FOCUS.value,
                reset_fg=Fg.RESET.value,
            ))
        return self

    def __input_version(self) -> Init:
        version: str = input('Develop version ' + Fg.SUCCESS.value + '0.0.0' + Fg.RESET.value + ' : ')
        self.state_handler.state.version = Version.from_str(version if version else '0.0.0')
        return self

    def __input_level(self) -> Init:
        self.state_handler.state.level = Level.DEV
        return self

    def __input_schemes(self) -> Init:
        schemes: List[Schemes] = []
        for scheme in Schemes:
            add: str = input('With ' + scheme.value + ' y/' + Fg.SUCCESS.value + 'n' + Fg.RESET.value + ' : ')
            if add is 'y':
                schemes.append(scheme)

        self.state_handler.state.schemes = schemes
        return self

    def __write_file(self) -> Init:
        yml: str = self.state_handler.write_file()
        print("""#################################################
{fg_green}Write file : {path!s} 
{reset_fg}#################################################""".format(
            path=self.state_handler.file_path(),
            reset_fg=Fg.RESET.value,
            fg_green=Fg.SUCCESS.value
        )
        )
        print(yml)
        return self

    def __ensure_have_state(self) -> bool:
        if self.state_handler.file_exists():
            self.state_handler.load_file_config()
            print(
                """###############################################
{fg_yellow}Flexio Flow already initialized 
{reset_fg}###############################################
""".format(
                    fg_yellow=Fg.FOCUS.value,
                    reset_fg=Fg.RESET.value
                ))
            PrintColor.log(Fg.FOCUS.value + 'at : ' + self.state_handler.file_path().as_posix())
            PrintColor.log(Fg.FOCUS.value + 'with : ' + str(self.state_handler.state.to_dict()))
            use: str = input('Use this file ' + Fg.SUCCESS.value + 'y' + Fg.RESET.value + '/n : ')
            use = use if use else 'y'

            if use is 'y':
                return True
            else:
                self.state_handler.reset_state()

        self.__start_message().__input_version().__input_level().__input_schemes()
        print(self.state_handler.state.schemes)

        return False

    def __final_message(self) -> Init:
        print(
            """###############################################
{fg_yellow}Enjoy with Flexio FLow 
{reset_fg}###############################################
""".format(
                fg_yellow=Fg.FOCUS.value,
                reset_fg=Fg.RESET.value
            ))
        return self

    def __ensure_version_control_initialized(self):
        self.version_control.build_branch(Branches.MASTER).with_action(Actions.INIT).process()

    def process(self):
        if not self.__ensure_have_state():
            self.__ensure_version_control_initialized()

        self.__final_message()
