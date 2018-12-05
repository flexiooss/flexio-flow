from typing import Optional, Type
from Branches.BranchFactory import BranchFactory
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.FlowAction import FlowAction
from Branches.Branches import Branches
from Branches.Branch import Branch


class FlexioFlow:
    __branch: Optional[Branches]
    __action: FlowAction
    __state_handler: StateHandler

    def __init__(self,
                 action: FlowAction,
                 branch: Optional[Branches],
                 state_handler: StateHandler
                 ) -> None:
        self.__action = action
        self.__branch = branch
        self.__state_handler = state_handler

    def init_context(self):
        pass

    def process(self):
        if self.__branch is not None:
            print(repr(self.__state_handler.state))
            version_handler: Type[Branch] = BranchFactory.create(self.__branch, self.__state_handler).set_action(
                self.__action).process()
