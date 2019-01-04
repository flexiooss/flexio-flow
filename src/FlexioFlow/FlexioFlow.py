from typing import Optional, Type, Dict, Union

from Core.ConfigHandler import ConfigHandler
from FlexioFlow.StateHandler import StateHandler
from Branches.Actions.Actions import Actions
from Branches.Actions.Action import Action
from Branches.Branches import Branches
from Branches.Actions.ActionFactory import ActionFactory
from Schemes.Schemes import Schemes
from VersionControl.VersionController import VersionController
from VersionControl.VersionControl import VersionControl
from VersionControl.VersionControlFactory import VersionControlFactory
from pathlib import Path


class FlexioFlow:
    __state_handler: Optional[StateHandler] = None

    def __init__(self,
                 version_controller: VersionController,
                 action: Actions,
                 branch: Optional[Branches],
                 options: Dict[str, Union[str, Schemes]],
                 dir_path: Path,
                 config_handler: ConfigHandler
                 ) -> None:

        self.__version_controller: VersionController = version_controller
        self.__action: Actions = action
        self.__branch: Optional[Branches] = branch
        self.__options: Dict[str, Union[str, Schemes]] = options

        if not dir_path.is_dir():
            raise NotADirectoryError

        self.__dir_path: Path = dir_path
        self.__config_handler: ConfigHandler = config_handler

    def __ensure_state_handler(self):
        self.__state_handler = StateHandler(self.__dir_path)
        if self.__action not in [Actions.INIT]:
            self.__state_handler.load_file_config()

    def __ensure_config_handler(self):
        self.__config_handler.load_file_config()

    def process(self):
        self.__ensure_state_handler()
        self.__ensure_config_handler()

        version_control: Type[VersionControl] = VersionControlFactory.build(
            self.__version_controller,
            self.__state_handler
        )

        action: Type[Action] = ActionFactory.build(
            self.__action,
            version_control,
            self.__branch,
            self.__state_handler,
            self.__options,
            self.__config_handler
        )

        action.process()
