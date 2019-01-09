from __future__ import annotations

from FlexioFlow.Actions.IssueActions import IssueActions
from FlexioFlow.StateHandler import StateHandler
from typing import Dict

from VersionControl.VersionControl import VersionControl


class Issue:

    def __init__(self,
                 action: IssueActions,
                 state_handler: StateHandler,
                 version_control: VersionControl,
                 options: Dict[str, str],
                 ) -> None:
        self.action: IssueActions = action
        self.state_handler: StateHandler = state_handler
        self.version_control: VersionControl = version_control
        self.options: Dict[str, str] = options

    def process(self):
        if self.action is IssueActions.READ:
            print('read issue')
        elif self.action is IssueActions.COMMENT:
            print('comment issue')
