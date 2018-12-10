from __future__ import annotations
from FlexioFlow.Actions.Action import Action
from FlexioFlow.Actions.Actions import Actions


class Start(Action):
    def process(self):
        self.version_control.with_branch(self.branch).set_action(Actions.START).process()
