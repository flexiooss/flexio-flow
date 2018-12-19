from __future__ import annotations

from typing import List, Dict, Any, Union
from Schemes.Schemes import Schemes
from FlexioFlow.Level import Level
from FlexioFlow.Version import Version
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Issuers import Issuers


class State:
    __version: Version
    __level: Level
    __schemes: List[Schemes]
    __issues: List[Dict[Issuers, Issue]]

    def __init__(self) -> None:
        pass

    @property
    def version(self) -> Version:
        return self.__version

    @version.setter
    def version(self, v: Version):
        self.__version: Version = v

    @property
    def level(self) -> Level:
        return self.__level

    @level.setter
    def level(self, v: Level):
        if not isinstance(v, Level):
            raise TypeError('level should be an instance of FlexioFlow.Level')
        self.__level = v

    @property
    def schemes(self) -> List[Schemes]:
        return self.__schemes

    @schemes.setter
    def schemes(self, v: List[Schemes]):
        if not (isinstance(item, Schemes) for item in v):
            raise TypeError('schemes should be an instance of List[FlexioFlow.Scheme]')
        self.__schemes = v

    @property
    def issues(self) -> List[Dict[Issuers, Issue]]:
        return self.__issues

    @issues.setter
    def issues(self, v: List[Dict[Issuers, Issue]]):
        if not (isinstance(issuer, Issuers) and isinstance(issue, Issue) for issuer, issue in v):
            raise TypeError('issues should be an instance of List[Dict[Issuers, Issue]]')
        self.__issues = v

    def to_dict(self) -> Dict[str, Any]:
        return {
            'version': str(self.version),
            'level': self.level.value,
            'schemes': self.__schemeListValue(),
            'issues': self.__issuesListValue()
        }

    def next_major(self) -> Version:
        self.__version = self.__version.next_major()
        return self.__version

    def next_minor(self) -> Version:
        self.__version = self.__version.next_minor()
        return self.__version

    def next_patch(self) -> Version:
        self.__version = self.__version.next_patch()
        return self.__version

    def next_dev_patch(self) -> Version:
        self.__level = Level.DEV
        self.__version = self.__version.next_patch()
        return self.__version

    def next_dev_minor(self) -> Version:
        self.__level = Level.DEV
        self.__version = self.__version.reset_patch()
        self.__version = self.__version.next_minor()
        return self.__version

    def set_stable(self) -> State:
        self.__level = Level.STABLE
        return self

    def set_dev(self) -> State:
        self.__level = Level.DEV
        return self

    def __schemeListValue(self) -> List[str]:
        ret = []
        for scheme in self.schemes:
            ret.append(scheme.value)
        return ret

    def __issuesListValue(self) -> List[Dict[str, Union[str, int]]]:
        ret = []
        issuer: Issuers
        issue: Issue
        for issuer, issue in self.issues:
            number: int = 0 if issue.number is None else issue.number
            item: Dict[str, Union[str, int]] = dict()
            item[issuer.value] = number
            ret.append(item)
        return ret

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
