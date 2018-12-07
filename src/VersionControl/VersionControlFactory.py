from typing import Type
from VersionControl.VersionControl import VersionControl
from VersionControl.VersionController import VersionController
from VersionControl.GitFlow.GitFlow import GitFlow
from FlexioFlow.StateHandler import StateHandler

class VersionControlFactory:
    @staticmethod
    def create(versionController: VersionController, state_handler:StateHandler) -> Type[VersionControl]:
        if versionController is VersionController.GITFLOW:
            return GitFlow(state_handler)

        raise ValueError("Bad VersionControlFactory creation: " + versionController.value)
