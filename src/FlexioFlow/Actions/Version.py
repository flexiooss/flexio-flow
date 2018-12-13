from __future__ import annotations
from FlexioFlow.Version import Version
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from typing import List
from Exceptions.FileExistError import FileExistError
from FlexioFlow.Actions.Action import Action
from pathlib import Path
from VersionControl.VersionControl import VersionControl
from typing import Type
from FlexioFlow.Actions.Action import Action
from FlexioFlow.Actions.Actions import Actions
from VersionControl.Branches import Branches


class Version(Action):



    def process(self):
        print('Version')
        self.options
