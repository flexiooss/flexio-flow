from __future__ import annotations
from VersionControl.Branch import Branch
from FlexioFlow.Actions.Actions import Actions

class Hotfix(Branch):

    def process(self):
        if self.action is Actions.START:
            print('Hotfix start')
        if self.action is Actions.FINISH:
            print('Hotfix finish')
        print(self.__dict__)
