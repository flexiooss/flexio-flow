import os
from typing import Optional, Type, Dict
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.Actions.Actions import Actions
from FlexioFlow.Actions.Action import Action
from VersionControl.Branches import Branches
from FlexioFlow.Actions.Init import Init
from FlexioFlow.Actions.ActionFactory import ActionFactory
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
                 options: Dict[str, str],
                 dir_path: Path
                 ) -> None:

        self.__version_controller: VersionController = version_controller
        self.__action: Actions = action
        self.__branch: Optional[Branches] = branch
        self.__options: Dict[str, str] = options
        if not dir_path.is_dir():
            raise ValueError(dir_path + ' : Path not exists')
        # self.__dir_path: Path = dir_path.rstrip('/') + '/'
        self.__dir_path: Path = dir_path

    def __should_init_state_handler(self) -> bool:
        if self.__action not in [Actions.INIT]:
            self.__state_handler = StateHandler(self.__dir_path).load_file_config()
            print(str(self.__state_handler.state.version))
            return True
        return False

    def process(self):
        self.__should_init_state_handler()

        if self.__action is Actions.INIT:
            Init(self.__dir_path).process()

        else:
            version_control: Type[VersionControl] = VersionControlFactory.create(self.__version_controller,
                                                                                 self.__state_handler)
            action: Type[Action] = ActionFactory.create(
                self.__action,
                version_control,
                self.__branch,
                self.__state_handler,
                self.__options
            )

            action.process()
