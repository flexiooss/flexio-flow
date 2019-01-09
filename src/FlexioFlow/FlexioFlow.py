from __future__ import annotations

from typing import Optional, Type, Dict, Union

from Core.ConfigHandler import ConfigHandler
from Core.Core import Core
from FlexioFlow.StateHandler import StateHandler
from Branches.Actions.Actions import Actions as BranchActions
from Branches.Actions.Action import Action
from Branches.Branches import Branches
from Branches.Actions.ActionFactory import ActionFactory
from FlexioFlow.Subject import Subject
from Schemes.Schemes import Schemes
from VersionControl.VersionController import VersionController
from VersionControl.VersionControl import VersionControl
from VersionControl.VersionControlFactory import VersionControlFactory
from pathlib import Path
from FlexioFlow.Actions.Version import Version
from Core.Actions.Actions import Actions as ActionsCore


class FlexioFlow:
    __branch: Optional[Branches]
    __branch_action: Optional[BranchActions]
    __config_handler: ConfigHandler
    __core_action: Optional[ActionsCore]
    __dir_path: Path
    __options: Dict[str, Union[str, Schemes, bool]]
    __state_handler: Optional[StateHandler] = None
    __version_controller: VersionController

    def __init__(self, subject: Subject):
        self.subject: Subject = subject

    def set_environment(self,

                        version_controller: VersionController,
                        branch_action: Optional[BranchActions],
                        core_action: Optional[ActionsCore],
                        branch: Optional[Branches],
                        options: Dict[str, Union[str, Schemes, bool]],
                        dir_path: Path,
                        config_handler: ConfigHandler
                        ) -> FlexioFlow:

        self.__version_controller: VersionController = version_controller
        self.__branch_action: Optional[BranchActions] = branch_action
        self.__core_action: Optional[ActionsCore] = core_action
        self.__branch: Optional[Branches] = branch
        self.__options: Dict[str, Union[str, Schemes, bool]] = options

        if not dir_path.is_dir():
            raise NotADirectoryError

        self.__dir_path: Path = dir_path
        self.__config_handler: ConfigHandler = config_handler
        return self

    def __ensure_state_handler(self):
        self.__state_handler = StateHandler(self.__dir_path)
        if self.__branch_action not in [BranchActions.INIT]:
            self.__state_handler.load_file_config()

    def __ensure_config_handler(self):
        self.__config_handler.load_file_config()

    def __process_subject_core(self):
        if self.__core_action is None:
            raise ValueError('should have Action')
        Core(
            action=self.__core_action,
            options=self.__options,
            config_handler=self.__config_handler
        ).process()

    def __process_subject_version(self):
        Version(
            state_handler=StateHandler(self.__dir_path).load_file_config(),
            options=self.__options
        ).process()

    def __process_branch_action(self):
        if self.__branch_action is None:
            raise ValueError('should have Action')

        self.__ensure_state_handler()
        self.__ensure_config_handler()

        version_control: VersionControl = VersionControlFactory.build(
            self.__version_controller,
            self.__state_handler
        )

        action: Type[Action] = ActionFactory.build(
            action=self.__branch_action,
            version_control=version_control,
            branch=self.__branch,
            state_handler=self.__state_handler,
            options=self.__options,
            config_handler=self.__config_handler
        )

        action.process()

    def process(self):
        if self.subject is Subject.CORE:
            self.__process_subject_core()
        elif self.subject is Subject.VERSION:
            self.__process_subject_version()
        elif self.subject is Subject.BRANCH:
            self.__process_branch_action()
