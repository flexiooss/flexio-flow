from __future__ import annotations
from VersionControl.Release import Release as AbstractRelease
from Branches.Actions.Actions import Actions
from VersionControl.Git.Branches.Release.Finish import Finish
from VersionControl.Git.Branches.Release.PreCheck import PreCheck
from VersionControl.Git.Branches.Release.Start import Start


class Release(AbstractRelease):

    def process(self):
        if self.action is Actions.START:
            self.start_message('Release start')
            Start(self.state_handler, self.issue, self.is_major).process()

        elif self.action is Actions.FINISH:
            self.start_message('Release finish')
            Finish(self.state_handler, self.issue, self.options.get('keep-branch', False),
                   self.options.get('close_issue', False)).process()

        elif self.action is Actions.PRECHECK:
            self.start_message('Release precheck')
            PreCheck(self.state_handler, self.issue).process()

        else:
            raise NotImplementedError
