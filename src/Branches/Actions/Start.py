from __future__ import annotations

from Branches.Actions.Action import Action
from Branches.Actions.Actions import Actions
from Branches.Actions.IssuerRecipe.RelatedIssueTopicRecipe import RelatedIssueTopicRecipe
from VersionControlProvider.Issue import Issue


class Start(Action):

    def __process_without_issue(self):
        self.version_control.build_branch(self.branch).with_action(Actions.START).process()

    def __process_with_issue(self, issue: Issue):
        self.version_control.build_branch(self.branch).with_issue(issue).with_action(Actions.START).process()

    def process(self):
        issue: Issue = None
        if self.config_handler.has_issuer():
            issue = RelatedIssueTopicRecipe(self.state_handler, self.config_handler).process()
        if issue is not None:
            self.__process_with_issue(issue)
        else:
            self.__process_without_issue()
