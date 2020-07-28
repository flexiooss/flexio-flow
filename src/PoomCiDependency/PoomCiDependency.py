from __future__ import annotations
from typing import Dict, Union

from FlexioFlow.Options import Options
from FlexioFlow.StateHandler import StateHandler
from PoomCiDependency.Actions.Actions import Actions
from PoomCiDependency.Actions.FullRepositoryJsonAction import FullRepositoryJsonAction
from Schemes.Schemes import Schemes


class PoomCiDependency:

    def __init__(self, action: Actions, state_handler: StateHandler, options: Options):
        self.action: Actions = action
        self.state_handler: StateHandler = state_handler
        self.options: Options = options

    def process(self):
        if self.action is Actions.FULL_REPOSITORY_JSON:

            FullRepositoryJsonAction(self.state_handler, self.options).process()
        else:
            raise ValueError("Bad PoomCiDependency Action : " + self.action.name)
