from __future__ import annotations

from VersionControl.Branch import Branch
from Branches.Actions.Actions import Actions
from VersionControl.Git.Branches.Feature.Finish import Finish
from VersionControl.Git.Branches.Feature.Start import Start
from slugify import slugify
from sty import fg, bg


class Feature(Branch):
    __name: str = None

    def with_name(self, name: str) -> Feature:
        self.__name: str = slugify(name)
        return self

    def process(self):
        if self.action is Actions.START:

            if self.__name is None:
                default_name: str = slugify(self.issue.title) if self.issue is not None else ''
                name: str = input(fg.red + '[required]' + fg.rs + ' Feature branch name : ' + fg.green + default_name + fg.rs + ' ')
                name = name if name else default_name
            else:
                name = self.__name

            self.start_message('Feature start : ' + name)

            Start(
                state_handler=self.state_handler,
                issue=self.issue,
                name=name
            ).process()

        elif self.action is Actions.FINISH:
            self.start_message('Feature finish')
            Finish(self.state_handler, self.issue).process()
        else:
            raise NotImplementedError
