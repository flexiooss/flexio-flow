from __future__ import annotations

from VersionControl.Branch import Branch
from Branches.Actions.Actions import Actions
from VersionControl.Git.Branches.Develop.Init import Init


class Develop(Branch):

    def process(self):
        if self.action is Actions.INIT:
            self.start_message('Develop Init')
            Init(self.state_handler, self.config_handler).process()
        else:
            raise NotImplementedError
