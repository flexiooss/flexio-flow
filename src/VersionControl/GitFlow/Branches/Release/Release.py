from __future__ import annotations

from VersionControl.GitFlow.Branches.Branch import Branch
from FlexioFlow.Actions.Actions import Actions


class Release(Branch):

    def process(self):
        if self.action is Actions.START:
            print('Release start')
        if self.action is Actions.FINISH:
            print('Release finish')
        if self.action is Actions.PLAN:
            print('Release plan')
        print(self.__dict__)
