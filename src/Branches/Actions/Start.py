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

from VersionControlProvider.Topic import Topic


class Start(Action):

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

    def __with_action(self, branch: Branch) -> Branch:
        return branch.with_action(Actions.START)

    def options(self, branch: Branch) -> Branch:
        return branch.with_options(self.options)

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

        topic: Optional[Topic] = None
        issue: Optional[Issue] = None
        branch: Optional[Branch] = None

        if self.config_handler.has_issuer():
            issue = RelatedIssueTopicRecipe(self.state_handler, self.config_handler, self.branch).process()

        branch = self.version_control.build_branch(self.branch)
        branch = self.__with_action(branch)
        branch = self.__with_issue(branch, issue)
        branch = self.__with_topic(branch, topic)
        branch = self.__ensure_is_major(branch)

        branch = self.__ensure_name(branch)
        branch.process()
