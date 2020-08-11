from __future__ import annotations

from pprint import pprint

from Branches.Actions.Issuer.IssueBuilder import IssueBuilder
from Core.ConfigHandler import ConfigHandler
from FlexioFlow.Actions.IssueActions import IssueActions
from FlexioFlow.Options import Options
from FlexioFlow.StateHandler import StateHandler
from typing import Dict, Optional

from Log.Log import Log
from VersionControl.VersionControl import VersionControl
from VersionControlProvider.Issue import Issue as AbstractIssue


class Issue:

    def __init__(self,
                 action: IssueActions,
                 state_handler: StateHandler,
                 version_control: VersionControl,
                 config_handler: ConfigHandler,
                 options: Options,
                 ) -> None:
        self.action: IssueActions = action
        self.state_handler: StateHandler = state_handler
        self.version_control: VersionControl = version_control
        self.config_handler: ConfigHandler = config_handler
        self.options: Options = options

    def process(self):
        if self.action is IssueActions.READ:

            issuer_builder: issuer_builder = IssueBuilder(
                self.version_control,
                self.state_handler,
                self.config_handler,
                None,
                self.options
            )

            issue: Optional[AbstractIssue] = issuer_builder.find_issue_from_branch_name().issue()

            if issue is not None:
                Log.info('waiting... from github...')
                read_issue: Optional[AbstractIssue] = issuer_builder.issuer().read_issue_by_number(issue.number)
                if read_issue is not None:
                    pprint(read_issue.__dict__())

        elif self.action is IssueActions.COMMENT:
            raise NotImplementedError
