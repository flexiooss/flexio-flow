from __future__ import annotations

from typing import Optional

from Branches.Actions.Action import Action
from Branches.Actions.Actions import Actions
from Branches.Actions.IssuerRecipe.RelatedIssueTopicRecipe import RelatedIssueTopicRecipe
from Branches.Branches import Branches
from ConsoleColors.Fg import Fg
from Log.Log import Log
from VersionControl.Branch import Branch
from VersionControl.Release import Release
from VersionControlProvider.Issue import Issue
from slugify import slugify


class Start(Action):

    def __process_without_issue(self) -> Branch:
        return self.version_control.build_branch(self.branch).with_action(Actions.START).with_options(self.options)

    def __process_with_issue(self, issue: Issue) -> Branch:
        return self.version_control.build_branch(self.branch).with_issue(issue).with_action(Actions.START).with_options(
            self.options)

    def __ensure_name(self, branch: Branch) -> Branch:
        if self.branch is Branches.FEATURE:
            default_name: str = slugify(branch.issue.title) if branch.issue is not None else ''
            name: str = input(
                Fg.FAIL.value + '[required]' + Fg.RESET.value + ' Feature branch name : ' + Fg.NOTICE.value + default_name + Fg.RESET.value + ' ')
            name = name if name else default_name

            branch.with_name(name=name)
        return branch

    def __ensure_is_major(self, branch: Branch) -> Branch:
        if self.branch is Branches.RELEASE:
            is_major_b: bool = False

            if self.options.get('major') is None:
                if self.options.get('no-cli') is not True:
                    is_major: str = input(
                        ' Is major Release Y/N : ' + Fg.SUCCESS.value + 'N' + Fg.RESET.value + ' ')
                    is_major_b = True if is_major.capitalize() == 'Y' else False
            else:
                is_major_b = self.options.get('major') is True
                if is_major_b:
                    Log.info('Release option Major set from options')

            branch.with_major(is_major=is_major_b)
        return branch

    def process(self):

        issue: Optional[Issue] = None
        branch: Optional[Branch] = None

        if self.config_handler.has_issuer():
            issue = RelatedIssueTopicRecipe(self.state_handler, self.config_handler).process()

        if issue is not None:
            branch = self.__process_with_issue(issue)
        else:
            branch = self.__process_without_issue()

        branch = self.__ensure_is_major(branch)
        self.__ensure_name(branch).process()
