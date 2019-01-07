from __future__ import annotations
import abc
from typing import Optional, Dict, Type
from Core.ConfigHandler import ConfigHandler
from Branches.Branches import Branches
from VersionControl.VersionControl import VersionControl
from FlexioFlow.StateHandler import StateHandler


class Action(abc.ABC):

    def __init__(self,
                 version_control: VersionControl,
                 branch: Optional[Branches],
                 state_handler: StateHandler,
                 options: Dict[str, str],
                 config_handler: ConfigHandler
                 ) -> None:
        self.version_control: VersionControl = version_control
        self.branch: Optional[Branches] = branch
        self.state_handler: StateHandler = state_handler
        self.options: Dict[str, str] = options
        self.config_handler: ConfigHandler = config_handler

    @abc.abstractmethod
    def process(self):
        pass
