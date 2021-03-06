from __future__ import annotations

from typing import Optional, List

from Branches.Actions.Action import Action
from Branches.Actions.Actions import Actions
from Branches.Actions.Issuer.IssueBuilder import IssueBuilder
from Branches.Actions.Topicer.TopicBuilder import TopicBuilder
from Branches.Branches import Branches
from ConsoleColors.Fg import Fg
from Exceptions.NoBranchSelected import NoBranchSelected
from Log.Log import Log
from VersionControl.Branch import Branch
from VersionControl.Git.GitCmd import GitCmd
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

    def __with_topics(self, branch: Branch, topics: Optional[List[Topic]]) -> Branch:
        if topics is not None:
            return branch.with_topics(topics)
        else:
            return branch

    def __ensure_is_major(self, branch: Branch) -> Branch:
        if self.branch is Branches.RELEASE:
            if not self.version_control.is_current_branch_develop():
                raise NoBranchSelected('Checkout to develop branch before')
            is_major_b: bool = False

            if self.options.major is None and not self.options.default:
                if self.options.no_cli is not True:
                    is_major: str = input(
                        ' Is major Release Y/N : ' + Fg.SUCCESS.value + 'N' + Fg.RESET.value + ' ')
                    is_major_b = True if is_major.capitalize() == 'Y' else False
                    self.options.major = is_major_b

            else:
                is_major_b = self.options.major is True
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

    def __ensure_stash_start(self):
        if not self.options.auto_stash and not self.options.default:
            if self.options.no_cli is not True:
                auto_stash: str = input(
                    ' Stash your working tree Y/N : ' + Fg.SUCCESS.value + 'N' + Fg.RESET.value + ' ')
                auto_stash_b = True if auto_stash.capitalize() == 'Y' else False
                self.options.auto_stash = auto_stash_b

        if self.options.auto_stash:
            self.version_control.stash_start()
            Log.info('Working tree stashed')

    def __ensure_stash_end(self):
        if self.options.auto_stash:
            self.version_control.stash_end()
            Log.info('Stashed work restored ')

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

        topics: Optional[List[Topic]] = topic_builder.try_ensure_topic().topics()

        if issue is not None and topics is not None and len(topics) > 0:
            topic_builder.attach_issue(issue)
            for topic in topics:
                issuer_builder.comment_issue_with_topic(topic)

        branch = self.__with_issue(branch, issue)
        branch = self.__with_topics(branch, topics)
        branch = self.__ensure_name(branch)
        self.__ensure_stash_start()
        branch.process()
        self.__ensure_stash_end()
