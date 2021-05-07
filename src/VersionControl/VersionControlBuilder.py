from VersionControl.VersionControl import VersionControl
from VersionControl.VersionController import VersionController
from VersionControl.Git.Git import Git
from FlexioFlow.StateHandler import StateHandler
from Core.ConfigHandler import ConfigHandler


class VersionControlBuilder:
    @staticmethod
    def build(version_controller: VersionController, state_handler: StateHandler,config_handler: ConfigHandler) -> VersionControl:
        if version_controller is VersionController.GIT:
            return Git(state_handler,config_handler)

        raise NotImplementedError
