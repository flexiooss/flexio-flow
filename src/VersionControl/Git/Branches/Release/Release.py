from __future__ import annotations
from VersionControl.Release import Release as AbstractRelease
from Branches.Actions.Actions import Actions
from VersionControl.Git.Branches.Release.Finish import Finish
from VersionControl.Git.Branches.Release.PreCheck import PreCheck
from VersionControl.Git.Branches.Release.Start import Start


class Release(AbstractRelease):

    def process(self):
        if self.action is Actions.START:
            self.start_message('Release start')

            Start(
                state_handler=self.state_handler,
                config_handler=self.config_handler,
                issue=self.issue,
                topics=self.topics,
                is_major=self.is_major
            ).process()

        elif self.action is Actions.FINISH:
            self.start_message('Release finish')

            Finish(
                state_handler=self.state_handler,
                config_handler=self.config_handler,
                issue=self.issue,
                topics=self.topics,
                keep_branch=self.options.keep_branch,
                close_issue=self.options.close_issue
            ).process()

        elif self.action is Actions.PRECHECK:
            self.start_message('Release precheck')

            PreCheck(
                state_handler=self.state_handler,
                config_handler=self.config_handler,
                issue=self.issue,
                topics=self.topics
            ).process()

        else:
            raise NotImplementedError
