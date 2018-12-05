from typing import Optional, Type, Dict
from Branches.BranchFactory import BranchFactory
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.FlowAction import FlowAction
from Branches.Branches import Branches
from Branches.Branch import Branch


class FlexioFlow:

    def __init__(self,
                 action: FlowAction,
                 branch: Optional[Branches],
                 options: Dict[str, str],
                 state_handler: StateHandler

                 ) -> None:
        self.__action: FlowAction = action
        self.__branch: Optional[Branches] = branch
        self.__options: Dict[str, str] = options
        self.__state_handler: StateHandler = state_handler

    def init_context(self):
        pass

    def process(self):
        if self.__branch is not None:
            print(repr(self.__state_handler.state))
            version_handler: Type[Branch] = BranchFactory.create(self.__branch, self.__state_handler).set_action(
                self.__action).process()
