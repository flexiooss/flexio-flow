from typing import Optional

from Branches.Branches import Branches
from Core.ConfigHandler import ConfigHandler
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.IssueDefault import IssueDefault


class IssueDefaultBuilder:
    def build(self, state_handler: StateHandler, config_handler: ConfigHandler,
              branch: Optional[Branches]) -> IssueDefault:

        issue: IssueDefault = IssueDefault()
        issue.assignees = [config_handler.config.github.user]

        if branch is Branches.RELEASE:
            issue.title = 'Release ' + str(state_handler.state.version)
            issue.labels = ['release']

        if branch is Branches.FEATURE:
            issue.labels = ['enhancement']

        if branch is Branches.HOTFIX:
            issue.labels = ['bug']

        return issue
