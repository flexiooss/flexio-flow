from __future__ import annotations

from Branches.Branch import Branch
from FlexioFlow.FlowAction import FlowAction


class Release(Branch):

    def process(self):
        if self.action is FlowAction.START:
            print('Release start')
        if self.action is FlowAction.FINISH:
            print('Release finish')
        if self.action is FlowAction.PLAN:
            print('Release plan')
        print(self.__dict__)
