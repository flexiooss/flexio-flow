from __future__ import annotations
from Branches.Branch import Branch
from typing import TypeVar
from FlexioFlow.FlowAction import FlowAction

class Hotfix(Branch):

    def process(self):
        if self.action is FlowAction.START:
            print('Hotfix start')
        if self.action is FlowAction.FINISH:
            print('Hotfix finish')
        print(self.__dict__)
