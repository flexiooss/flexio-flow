from __future__ import annotations

from Branches.Actions.Action import Action
from Branches.Actions.Actions import Actions
from Branches.Actions.IssuerRecipe.RelatedIssueTopicRecipe import RelatedIssueTopicRecipe
from Branches.Branches import Branches
from VersionControl.Branch import Branch
from VersionControlProvider.Issue import Issue


class Start(Action):

    def __process_without_issue(self):
        self.version_control.build_branch(self.branch).with_action(Actions.START).process()

    def __process_with_issue(self, issue: Issue):
        self.version_control.build_branch(self.branch).with_issue(issue).with_action(Actions.START).process()

    def __ensure_name(self, branch: Branch) -> Branch:
        if self.branch is Branches.FEATURE:
            pass
        #TODO input name
        return branch

    def process(self):

        issue: Issue = None
        branch: Branch = None

        if self.config_handler.has_issuer():
            issue = RelatedIssueTopicRecipe(self.state_handler, self.config_handler).process()

        if issue is not None:
            branch: Branch = self.__process_with_issue(issue)
        else:
            branch: Branch = self.__process_without_issue()

        self.__ensure_name(branch).process()
