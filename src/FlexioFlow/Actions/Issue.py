from __future__ import annotations

from Core.ConfigHandler import ConfigHandler
from Core.IssuerHandler import IssuerHandler
from FlexioFlow.Actions.IssueActions import IssueActions
from FlexioFlow.StateHandler import StateHandler
from typing import Dict

from VersionControl.VersionControl import VersionControl
from VersionControlProvider.Issuer import Issuer
from VersionControlProvider.Issue import Issue as AbstractIssue


class Issue:

    def __init__(self,
                 action: IssueActions,
                 state_handler: StateHandler,
                 version_control: VersionControl,
                 config_handler: ConfigHandler,
                 options: Dict[str, str],
                 ) -> None:
        self.action: IssueActions = action
        self.state_handler: StateHandler = state_handler
        self.version_control: VersionControl = version_control
        self.config_handler: ConfigHandler = config_handler
        self.options: Dict[str, str] = options

    def process(self):
        if self.action is IssueActions.READ:
            print('read issue')
            issue_number = self.version_control.get_issue_number()
            print(issue_number)

            issuer: Issuer = IssuerHandler(
                state_handler=self.state_handler,
                config_handler=self.config_handler).issuer()

            issue : AbstractIssue = issuer.read_issue_by_number(int(issue_number))
            print(issue.__dict__())



        elif self.action is IssueActions.COMMENT:
            print('comment issue')
