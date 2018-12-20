from __future__ import annotations

from VersionControl.Branch import Branch
from FlexioFlow.Actions.Actions import Actions
from VersionControl.GitFlow.Branches.Master.Init import Init


class Master(Branch):

    def process(self):
        if self.action is Actions.INIT:
            self.start_message('Master Init')
            Init(self.state_handler).process()
        else:
            raise NotImplementedError
