from __future__ import annotations

import re
from typing import Optional, Type, Tuple, Match, List
from FlexioFlow.Level import Level
from FlexioFlow.Version import Version
from Branches.BranchesConfig import BranchesConfig
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic


class BranchHandler:

    def __init__(self, branch: str, branches: BranchesConfig):
        self.branch: str = branch
        self.branches: BranchesConfig = branches
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
        if self.branches.is_hotfix(self.branch):
            return self.__format_branch_name('/'.join([
                self.branch,
                '-'.join([str(version), Level.DEV.value])
            ]))
        elif self.branches.is_release(self.branch):
            return self.__format_branch_name('/'.join([self.branch, str(version)]))
        else:
            return self.branch

    def branch_name_from_version_with_name(self, version: Version, name: str) -> str:
        if self.branches.is_feature(self.branch):
            return self.__format_branch_name('/'.join([
                self.branch,
                '-'.join([name, str(version), Level.DEV.value])
            ]))
        else:
            return self.branch

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
