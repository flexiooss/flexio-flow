from __future__ import annotations

from typing import Optional

from Branches.Actions.Action import Action
from Branches.Actions.Actions import Actions
from Branches.Actions.Issuer.IssueBuilder import IssueBuilder
from Branches.Actions.Topicer.TopicBuilder import TopicBuilder
from Branches.Branches import Branches
from ConsoleColors.Fg import Fg
from Log.Log import Log
from VersionControl.Branch import Branch
from VersionControlProvider.Issue import Issue
from slugify import slugify

from VersionControlProvider.Topic import Topic


class Start(Action):

    def __with_action(self, branch: Branch) -> Branch:
        return branch.with_action(Actions.START)

    def __with_options(self, branch: Branch) -> Branch:
        return branch.with_options(self.options)

    def __with_issue(self, branch: Branch, issue: Issue) -> Branch:
        if issue is not None:
            return branch.with_issue(issue)
        else:
            return branch

    def __with_topic(self, branch: Branch, topic: Topic) -> Branch:
        if topic is not None:
            return branch.with_topic(topic)
        else:
            return branch

    def __ensure_is_major(self, branch: Branch) -> Branch:
        if self.branch is Branches.RELEASE:
            is_major_b: bool = False

            if self.options.get('major') is None:
                if self.options.get('no-cli') is not True:
                    is_major: str = input(
                        ' Is major Release Y/N : ' + Fg.SUCCESS.value + 'N' + Fg.RESET.value + ' ')
                    is_major_b = True if is_major.capitalize() == 'Y' else False
                    self.options.update({'major': is_major_b})

            else:
                is_major_b = self.options.get('major') is True
                if is_major_b:
                    Log.info('Release option Major set from options')

            branch.with_major(is_major=is_major_b)
        return branch

    def __ensure_name(self, branch: Branch) -> Branch:
        if self.branch is Branches.FEATURE:
            default_name: str = slugify(branch.issue.title) if branch.issue is not None else ''
            name: str = input(
                Fg.FAIL.value + '[required]' + Fg.RESET.value + ' Feature branch name : ' + Fg.NOTICE.value + default_name + Fg.RESET.value + ' ')
            name = name if name else default_name

            branch.with_name(name=name)
        return branch

    def process(self):
        branch: Branch = self.version_control.build_branch(self.branch)
        branch = self.__with_action(branch)
        branch = self.__ensure_is_major(branch)
        branch = self.__with_options(branch)

        issuer_builder: issuer_builder = IssueBuilder(
            self.version_control,
            self.state_handler,
            self.config_handler,
            self.branch,
            self.options
        )

        issue: Optional[Issue] = issuer_builder.try_ensure_issue().issue()

        topic_builder: TopicBuilder = TopicBuilder(
            self.version_control,
            self.state_handler,
            self.config_handler,
            self.branch,
            self.options
        )

        topic: Optional[Topic] = topic_builder.try_ensure_topic().topic()

        if issue is not None and topic is not None:
            issuer_builder.comment_issue_with_topic(topic)
            topic_builder.attach_issue(issue)

        branch = self.__with_issue(branch, issue)
        branch = self.__with_topic(branch, topic)
        branch = self.__ensure_name(branch)
        branch.process()
