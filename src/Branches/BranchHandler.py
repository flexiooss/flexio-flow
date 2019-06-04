from __future__ import annotations

import re
from typing import Optional, Type, Tuple, Match
from FlexioFlow.Level import Level
from FlexioFlow.Version import Version
from Branches.Branches import Branches
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic


class BranchHandler:

    def __init__(self, branch: Branches):
        self.branch: Branches = branch
        self.issue: Optional[Issue] = None
        self.topic: Optional[Topic] = None

    def with_issue(self, issue: Optional[Issue]) -> BranchHandler:
        self.issue = issue
        return self

    def with_topic(self, topic: Optional[Topic]) -> BranchHandler:
        self.topic = topic
        return self

    def __format_branch_name(self, name: str) -> str:
        return "{name!s}{topic_ref!s}{issue_ref!s}".format(
            name=name,
            topic_ref=self.topic.get_ref() if self.topic is not None else '',
            issue_ref=self.issue.get_ref() if self.issue is not None else ''
        )

    def branch_name_from_version(self, version: Optional[Version] = None) -> str:
        if self.branch is Branches.HOTFIX:
            return self.__format_branch_name('/'.join([
                Branches.HOTFIX.value,
                '-'.join([str(version), Level.DEV.value])
            ]))
        elif self.branch is Branches.RELEASE:
            return self.__format_branch_name('/'.join([Branches.RELEASE.value, str(version)]))
        else:
            return self.branch.value

    def branch_name_from_version_with_name(self, version: Version, name: str) -> str:
        if self.branch is Branches.FEATURE:
            return self.__format_branch_name('/'.join([
                Branches.FEATURE.value,
                '-'.join([name, str(version), Level.DEV.value])
            ]))
        else:
            return self.branch.value

    @staticmethod
    def issue_number_from_branch_name(name: str) -> Optional[int]:
        regexp = re.compile('[\w_\/\d-]*(?:#(?P<issue_number>[\d]+))$')
        matches: Match = re.match(regexp, name)
        if matches is None:
            return None
        else:
            return matches.groupdict().get('issue_number')

    @staticmethod
    def topic_number_from_branch_name(name: str) -> Optional[int]:
        regexp = re.compile('[\w_\/\d-]*(?:##(?P<topic_number>[\d]+))')
        matches: Match = re.match(regexp, name)
        if matches is None:
            return None
        else:
            return matches.groupdict().get('topic_number')
