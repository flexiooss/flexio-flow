from typing import Optional, Type
from Branches.BranchFactory import BranchFactory
from FlexioFlow.FlexioFlowObjectHandler import FlexioFlowObjectHandler
from FlexioFlow.FlowAction import FlowAction
from Branches.Branches import Branches
from Branches.Branch import Branch


class FlexioFlow:
    __branch: Optional[Branches]
    __action: FlowAction
    __flow_object_handler: FlexioFlowObjectHandler

    def __init__(self,
                 action: FlowAction,
                 branch: Optional[Branches],
                 flow_object_handler: FlexioFlowObjectHandler
                 ) -> None:
        self.__action = action
        self.__branch = branch
        self.__flow_object_handler = flow_object_handler

    def init_context(self):
        pass

    def process(self):
        if self.__branch is not None:
            print(repr(self.__flow_object_handler.state))
            version_handler: Type[Branch] = BranchFactory.create(self.__branch).set_action(self.__action).process()
