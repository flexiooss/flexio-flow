from __future__ import annotations
from Branches.Actions.Action import Action
from Branches.Actions.Actions import Actions


class Finish(Action):

    def process(self):
        self.version_control.build_branch(self.branch).with_action(Actions.FINISH).with_options(self.options).process()
