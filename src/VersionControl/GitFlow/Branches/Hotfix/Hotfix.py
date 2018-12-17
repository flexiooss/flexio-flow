from __future__ import annotations

from VersionControl.Branch import Branch
from FlexioFlow.Actions.Actions import Actions
from VersionControl.GitFlow.Branches.Hotfix.Finish import Finish
from VersionControl.GitFlow.Branches.Hotfix.Start import Start


class Hotfix(Branch):

    def process(self):
        if self.action is Actions.START:
            print('Hotfix start')
            Start(self.state_handler).process()
        if self.action is Actions.FINISH:
            print('Hotfix finish')
            Finish(self.state_handler).process()
        print(self.__dict__)
