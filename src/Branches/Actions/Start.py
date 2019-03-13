from __future__ import annotations

from Branches.Actions.Action import Action
from Branches.Actions.Actions import Actions
from Branches.Actions.IssuerRecipe.RelatedIssueTopicRecipe import RelatedIssueTopicRecipe
from Branches.Branches import Branches
from ConsoleColors.Fg import Fg
from VersionControl.Branch import Branch
from VersionControlProvider.Issue import Issue
from slugify import slugify


class Start(Action):

    def __process_without_issue(self) -> Branch:
        return self.version_control.build_branch(self.branch).with_action(Actions.START)

    def __process_with_issue(self, issue: Issue) -> Branch:
        return self.version_control.build_branch(self.branch).with_issue(issue).with_action(Actions.START)

    def __ensure_name(self, branch: Branch) -> Branch:
        if self.branch is Branches.FEATURE:
            default_name: str = slugify(branch.issue.title) if branch.issue is not None else ''
            name: str = input(
                Fg.FAIL.value + '[required]' + Fg.RESET.value + ' Feature branch name : ' + Fg.NOTICE.value + default_name + Fg.RESET.value + ' ')
            name = name if name else default_name

            branch.with_name(name=name)
        return branch

    def process(self):

        issue: Issue = None
        branch: Branch = None

        if self.config_handler.has_issuer():
            issue = RelatedIssueTopicRecipe(self.state_handler, self.config_handler).process()

        if issue is not None:
            branch = self.__process_with_issue(issue)
        else:
            branch = self.__process_without_issue()

        self.__ensure_name(branch).process()
