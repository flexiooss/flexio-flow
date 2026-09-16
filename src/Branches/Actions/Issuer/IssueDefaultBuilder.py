from typing import Optional, Dict

from Branches.Branches import Branches
from Core.ConfigHandler import ConfigHandler
from FlexioFlow.Options import Options
from FlexioFlow.Version import Version
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.IssueDefault import IssueDefault


class IssueDefaultBuilder:
    def build(self,
              state_handler: StateHandler,
              config_handler: ConfigHandler,
              branch: Optional[Branches],
              options: Options
              ) -> IssueDefault:

        issue: IssueDefault = IssueDefault()
        issue.assignees = [config_handler.config.github.user]

        if branch is Branches.RELEASE:

            version: Version = state_handler.state.version.next_major() if options.major is True else state_handler.state.version

            issue.title = 'Release ' + str(version)
            issue.labels = ['release']

        if branch is Branches.FEATURE:
            if options.branch_name is not None:
                issue.title = options.branch_name
            issue.labels = ['enhancement']

        if branch is Branches.HOTFIX:
            issue.title = 'Hotfix ' + str(state_handler.get_next_patch_version())
            issue.labels = ['bug', 'hotfix']

        return issue
