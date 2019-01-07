from __future__ import annotations

from VersionControl.Branch import Branch
from Branches.Actions.Actions import Actions
from VersionControl.Git.Branches.Master.Init import Init


class Master(Branch):

    def process(self):
        if self.action is Actions.INIT:
            self.start_message('Master Init')
            Init(self.state_handler).process()
        else:
            raise NotImplementedError
