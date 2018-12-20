from typing import Type
from VersionControl.VersionControl import VersionControl
from VersionControl.VersionController import VersionController
from VersionControl.GitFlow.GitFlow import GitFlow
from FlexioFlow.StateHandler import StateHandler

class VersionControlFactory:
    @staticmethod
    def build(version_controller: VersionController, state_handler:StateHandler) -> VersionControl:
        if version_controller is VersionController.GITFLOW:
            return GitFlow(state_handler)

        raise NotImplementedError
