from __future__ import annotations

from Branches.Actions.Actions import Actions
from VersionControl.Branch import Branch
from VersionControl.Git.Branches.SupportBranch.Finish import Finish
from VersionControl.Git.Branches.SupportBranch.Start import Start


class SupportBranch(Branch):

    def process(self):
        if self.action is Actions.START:
            self.start_message('Support branch start')
            Start(
                state_handler=self.state_handler,
                config_handler=self.config_handler,
                issue=self.issue,
                topics=self.topics,
                options=self.options
            ).process()

        elif self.action is Actions.FINISH:
            self.start_message('Support branch finish')
            Finish(
                state_handler=self.state_handler,
                config_handler=self.config_handler,
                issue=self.issue,
                topics=self.topics,
                keep_branch=self.options.keep_branch,
                close_issue=self.options.close_issue,
                options=self.options
            ).process()

        else:
            raise NotImplementedError
