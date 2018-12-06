from typing import Optional, Type, Dict
from Branches.BranchFactory import BranchFactory
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.FlowAction import FlowAction
from Branches.Branches import Branches
from Branches.Branch import Branch
from FlexioFlow.Actions.Init import Init
import os


class FlexioFlow:
    __state_handler: Optional[StateHandler] = None

    def __init__(self,
                 action: FlowAction,
                 branch: Optional[Branches],
                 options: Dict[str, str],
                 dir_path: str
                 ) -> None:
        self.__action: FlowAction = action
        self.__branch: Optional[Branches] = branch
        self.__options: Dict[str, str] = options
        if not os.path.exists(dir_path):
            raise ValueError(dir_path + ' : Path not exists')
        self.__dir_path: str = dir_path.rstrip('/') + '/'

    def __should_init_state_handler(self) -> bool:
        if self.__action not in [FlowAction.INIT]:
            self.__state_handler = StateHandler(self.__dir_path).load_file_config()
            print(str(self.__state_handler.state.version))
            return True
        return False

    def process(self):
        self.__should_init_state_handler()

        if self.__action is FlowAction.INIT:
            Init(self.__dir_path).process()

        elif self.__branch is not None:
            print(repr(self.__state_handler.state))
            branch_handler: Type[Branch] = BranchFactory.create(self.__branch, self.__state_handler).set_action(
                self.__action).process()
