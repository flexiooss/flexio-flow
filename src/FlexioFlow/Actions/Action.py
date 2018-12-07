from __future__ import annotations
import abc
from typing import Optional, Dict
from VersionControl.Branches import Branches
from VersionControl.VersionControl import VersionControl
from FlexioFlow.StateHandler import StateHandler


class Action:

    def __init__(self,
                 version_control: VersionControl,
                 branch: Optional[Branches],
                 state_handler: StateHandler,
                 options: Dict[str, str]
                 ):
        self.version_control: VersionControl = version_control
        self.branch: Optional[Branches] = branch
        self.state_handler: StateHandler = state_handler
        self.options: Dict[str, str] = options

    @abc.abstractmethod
    def process(self):
        pass
