from __future__ import annotations
from VersionControl.Branch import Branch
from FlexioFlow.Actions.Actions import Actions
from VersionControl.GitFlow.Branches.Release.Finish import Finish
from VersionControl.GitFlow.Branches.Release.PreCheck import PreCheck
from VersionControl.GitFlow.Branches.Release.Start import Start


class Release(Branch):

    def process(self):
        if self.action is Actions.START:
            print('Release start')
            Start(self.state_handler).process()
        if self.action is Actions.FINISH:
            print('Release finish')
            Finish(self.state_handler).process()
        if self.action is Actions.PRECHECK:
            print('Release precheck')
            PreCheck(self.state_handler).process()
        print(self.__dict__)
