from __future__ import annotations
from VersionControl.Branch import Branch
from Branches.Actions.Actions import Actions
from VersionControl.Git.Branches.Release.Finish import Finish
from VersionControl.Git.Branches.Release.PreCheck import PreCheck
from VersionControl.Git.Branches.Release.Start import Start


class Release(Branch):



    def process(self):
        if self.action is Actions.START:
            self.start_message('Release start')
            Start(self.state_handler, self.issue).process()
        elif self.action is Actions.FINISH:
            self.start_message('Release finish')
            Finish(self.state_handler, self.issue).process()
        elif self.action is Actions.PRECHECK:
            self.start_message('Release precheck')
            PreCheck(self.state_handler).process()
        else:
            raise NotImplementedError
