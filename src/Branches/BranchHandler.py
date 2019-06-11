from __future__ import annotations

import re
from typing import Optional, Type, Tuple, Match, List
from FlexioFlow.Level import Level
from FlexioFlow.Version import Version
from Branches.Branches import Branches
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic


class BranchHandler:

    def __init__(self, branch: Branches):
        self.branch: Branches = branch
        self.issue: Optional[Issue] = None
        self.topics: Optional[List[Topic]] = None

    def with_issue(self, issue: Optional[Issue]) -> BranchHandler:
        self.issue = issue
        return self

    def with_topics(self, topics: Optional[List[Topic]]) -> BranchHandler:
        self.topics = topics
        return self

    def __format_branch_name(self, name: str) -> str:
        topics_ref: str = ''

        if self.topics is not None and len(self.topics) > 0:
            for topic in self.topics:
                topics_ref += topic.get_ref()

        return "{name!s}{topics_ref!s}{issue_ref!s}".format(
            name=name,
            topics_ref=topics_ref,
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
        regexp = re.compile('[\w_\/\d\-\.#]*(?:(?:(?<=[^#])#(?=[^#]))(?P<issue_number>[\d]+)?)$')
        matches: Match = re.match(regexp, name)
        if matches is None:
            return None
        else:
            return int(matches.groupdict().get('issue_number'))

    @staticmethod
    def topics_number_from_branch_name(name: str) -> Optional[List[int]]:
        regexp = re.compile('[\w_\/\d\-\.]*(?:##(?P<topic_number>[\d]+))?')
        matches: List = re.findall(regexp, name)
        ret: List[int] = list(map(lambda x: int(x), filter(lambda x: len(x) > 0, map(lambda x: x.strip(), matches))))

        if len(ret) > 0:
            return ret
        else:
            return None
