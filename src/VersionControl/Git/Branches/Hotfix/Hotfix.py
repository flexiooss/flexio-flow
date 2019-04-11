from __future__ import annotations

from VersionControl.Branch import Branch
from Branches.Actions.Actions import Actions
from VersionControl.Git.Branches.Hotfix.Finish import Finish
from VersionControl.Git.Branches.Hotfix.Start import Start


class Hotfix(Branch):

    def process(self):
        if self.action is Actions.START:
            self.start_message('Hotfix start')
            Start(self.state_handler, self.issue).process()
        elif self.action is Actions.FINISH:
            self.start_message('Hotfix finish')
            Finish(self.state_handler, self.issue, self.options.get('keep-branch', False)).process()
        else:
            raise NotImplementedError
