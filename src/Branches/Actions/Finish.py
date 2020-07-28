from __future__ import annotations

from typing import Optional, List

from Branches.Actions.Action import Action
from Branches.Actions.Actions import Actions
from Branches.Actions.Issuer.IssueBuilder import IssueBuilder
from Branches.Actions.Topicer.TopicBuilder import TopicBuilder
from VersionControl.Branch import Branch
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Issuer import Issuer
from Core.IssuerHandler import IssuerHandler
from ConsoleColors.Fg import Fg
from VersionControlProvider.Topic import Topic


class Finish(Action):

    def __with_action(self, branch: Branch) -> Branch:
        return branch.with_action(Actions.FINISH)

    def __with_options(self, branch: Branch) -> Branch:
        return branch.with_options(self.options)

    def __with_issue(self, branch: Branch, issue: Issue) -> Branch:
        if issue is not None:
            self.__should_close_issue()
            return branch.with_issue(issue)
        else:
            return branch

    def __with_topic(self, branch: Branch, topics: Optional[List[Topic]]) -> Branch:
        if topics is not None:
            return branch.with_topics(topics)
        else:
            return branch

    def __should_close_issue(self):
        close_issue_b: bool = True

        if not self.options.default:
            close_issue: str = input(
                ' Close Issue Y/N : ' + Fg.SUCCESS.value + 'Y' + Fg.RESET.value + ' ')
            close_issue_b = False if close_issue.capitalize() == 'N' else True

        if close_issue_b:
            self.options.close_issue = True

    def process(self):

        branch: Branch = self.version_control.build_branch(self.branch)
        branch = self.__with_action(branch)
        branch = self.__with_options(branch)

        issuer_builder: issuer_builder = IssueBuilder(
            self.version_control,
            self.state_handler,
            self.config_handler,
            self.branch,
            self.options
        )

        issue: Optional[Issue] = issuer_builder.find_issue_from_branch_name().issue()

        topic_builder: TopicBuilder = TopicBuilder(
            self.version_control,
            self.state_handler,
            self.config_handler,
            self.branch,
            self.options
        )

        topics: Optional[List[Topic]] = topic_builder.find_topic_from_branch_name().topics()

        branch = self.__with_issue(branch, issue)
        branch = self.__with_topic(branch, topics)
        branch.process()
