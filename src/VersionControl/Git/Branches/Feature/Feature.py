from __future__ import annotations

from VersionControl.Branch import Branch
from Branches.Actions.Actions import Actions
from VersionControl.Git.Branches.Feature.Finish import Finish
from VersionControl.Git.Branches.Feature.Start import Start
from slugify import slugify


class Feature(Branch):

    def with_name(self, name: str) -> Feature:
        self.name: str = slugify(name)
        return self

    def process(self):
        if self.action is Actions.START:

            self.start_message('Feature start : ' + self.name)

            Start(
                state_handler=self.state_handler,
                issue=self.issue,
                name=self.name
            ).process()

        elif self.action is Actions.FINISH:
            self.start_message('Feature finish')
            Finish(self.state_handler, self.issue).process()
        else:
            raise NotImplementedError
