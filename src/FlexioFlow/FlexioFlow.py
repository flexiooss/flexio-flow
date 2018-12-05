from typing import Optional
from VersionFlowStep.VersionFlowStepFactory import VersionFlowStepFactory
from FlexioFlow.FlexioFlowObjectHandler import FlexioFlowObjectHandler
from FlexioFlow.FlowAction import FlowAction
from FlexioFlow.VersionFlowStep import VersionFlowStep


class FlexioFlow:
    __version_flow: Optional[VersionFlowStep]
    __action: FlowAction
    __flexio_flow_object_handler: FlexioFlowObjectHandler

    def __init__(self,
                 action: FlowAction,
                 version_flow: Optional[VersionFlowStep],
                 flexio_flow_object_handler: FlexioFlowObjectHandler
                 ) -> None:
        self.__action = action
        self.__version_flow = version_flow
        self.__flexio_flow_object_handler = flexio_flow_object_handler

    def initContext(self):
        pass

    def process(self):
        if self.__version_flow is not None:
            print(repr(self.__flexio_flow_object_handler.state))
            # VersionFlowStepFactory() \
            #     .get(self.__version_flow) \
            #     .action(self.__action) \
            #     .process()
