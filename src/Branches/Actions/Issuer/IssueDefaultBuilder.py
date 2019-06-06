from typing import Optional, Dict

from Branches.Branches import Branches
from Core.ConfigHandler import ConfigHandler
from FlexioFlow.Version import Version
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.IssueDefault import IssueDefault


class IssueDefaultBuilder:
    def build(self,
              state_handler: StateHandler,
              config_handler: ConfigHandler,
              branch: Optional[Branches],
              options: Dict[str, str]
              ) -> IssueDefault:

        issue: IssueDefault = IssueDefault()
        issue.assignees = [config_handler.config.github.user]

        if branch is Branches.RELEASE:

            version: Version = state_handler.state.version.next_major() if options.get(
                'major') is True else state_handler.state.version

            issue.title = 'Release ' + str(version)
            issue.labels = ['release']

        if branch is Branches.FEATURE:
            issue.labels = ['enhancement']

        if branch is Branches.HOTFIX:
            issue.labels = ['bug', 'hotfix']

        return issue
