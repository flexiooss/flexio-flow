from __future__ import annotations

from VersionControl.Branch import Branch
from Branches.Actions.Actions import Actions
from VersionControl.Git.Branches.Hotfix.Finish import Finish
from VersionControl.Git.Branches.Hotfix.Start import Start


class Hotfix(Branch):

    def process(self):
        if self.action is Actions.START:
            self.start_message('Hotfix start')
            Start(
                state_handler=self.state_handler,
                issue=self.issue,
                topics=self.topics
            ).process()

        elif self.action is Actions.FINISH:
            self.start_message('Hotfix finish')

            Finish(
                state_handler=self.state_handler,
                issue=self.issue,
                topics=self.topics,
                keep_branch=self.options.keep_branch,
                close_issue=self.options.close_issue
            ).process()

        else:
            raise NotImplementedError
