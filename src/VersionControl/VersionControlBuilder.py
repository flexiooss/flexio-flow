from VersionControl.VersionControl import VersionControl
from VersionControl.VersionController import VersionController
from VersionControl.Git.Git import Git
from FlexioFlow.StateHandler import StateHandler


class VersionControlBuilder:
    @staticmethod
    def build(version_controller: VersionController, state_handler: StateHandler) -> VersionControl:
        if version_controller is VersionController.GIT:
            return Git(state_handler)

        raise NotImplementedError
