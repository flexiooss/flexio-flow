from __future__ import annotations
from FlexioFlow.Actions.Action import Action
from FlexioFlow.Actions.Actions import Actions

class Finish(Action):
    def process(self):
        self.version_control.build_branch(self.branch).with_action(Actions.FINISH).process()

