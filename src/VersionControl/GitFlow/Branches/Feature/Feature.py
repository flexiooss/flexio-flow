from __future__ import annotations

from VersionControl.Branch import Branch
from FlexioFlow.Actions.Actions import Actions
from VersionControl.GitFlow.Branches.Feature.Finish import Finish
from VersionControl.GitFlow.Branches.Feature.Start import Start


class Feature(Branch):

    def process(self):
        if self.action is Actions.START:
            self.start_message('Feature start')
            Start(self.state_handler, self.issue).process()
        elif self.action is Actions.FINISH:
            self.start_message('Feature finish')
            Finish(self.state_handler, self.issue).process()
        else:
            raise NotImplementedError
