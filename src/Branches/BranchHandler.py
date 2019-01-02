from __future__ import annotations

import re
from typing import Optional, Type, Tuple, Match
from FlexioFlow.Level import Level
from FlexioFlow.Version import Version
from Branches.Branches import Branches
from VersionControlProvider.Issue import Issue


class BranchHandler:

    def __init__(self, branch: Branches):
        self.branch: Branches = branch
        self.issue: Optional[Type[Issue]] = None

    def with_issue(self, issue: Optional[Type[Issue]]) -> BranchHandler:
        self.issue = issue
        return self

    def __format_branch_name(self, version: str) -> str:
        return "{version!s}{issue_ref!s}".format(
            version=version,
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
                Branches.RELEASE.value,
                '-'.join([name, str(version)])
            ]))
        else:
            return self.branch.value

    @staticmethod
    def issue_number_from_branch_name(name: str) -> Optional[int]:
        regexp = re.compile('.*(?:#(?P<issue_number>[\d]+))$')
        matches: Match = re.match(regexp, name)
        if matches is None:
            return None
        else:
            return matches.groupdict().get('issue_number')
