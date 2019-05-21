from __future__ import annotations

from typing import Optional

from Branches.Actions.Action import Action
from Branches.Actions.Actions import Actions
from VersionControl.Branch import Branch
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Issuer import Issuer
from Core.IssuerHandler import IssuerHandler
from ConsoleColors.Fg import Fg


class Finish(Action):

    def __process_without_issue(self) -> Branch:
        return self.version_control.build_branch(self.branch).with_action(Actions.FINISH).with_options(self.options)

    def __should_close_issue(self):
        close_issue: str = input(
            ' Close Issue Y/N : ' + Fg.SUCCESS.value + 'Y' + Fg.RESET.value + ' ')
        close_issue_b = False if close_issue.capitalize() == 'N' else True
        if close_issue_b:
            self.options.update({'close_issue': True})

    def __process_with_issue(self, issue: Issue) -> Branch:
        self.__should_close_issue()

        return self.version_control.build_branch(self.branch).with_issue(issue).with_action(
            Actions.FINISH).with_options(self.options)

    def process(self):

        issue: Optional[Issue] = None
        branch: Optional[Branch] = None

        if self.config_handler.has_issuer():
            issue_number: Optional[int] = self.version_control.get_issue_number()
            if issue_number is not None:
                issuer: Issuer = IssuerHandler(self.state_handler, self.config_handler).issuer()
                issue = issuer.issue_builder().with_number(issue_number)

        if issue is not None:
            branch = self.__process_with_issue(issue)
        else:
            branch = self.__process_without_issue()

        branch.process()
