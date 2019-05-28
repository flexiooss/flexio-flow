from __future__ import annotations
import abc
from typing import Type, Optional

from Core.ConfigHandler import ConfigHandler
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.Github.Repo import Repo
from VersionControlProvider.Issue import Issue
from VersionControlProvider.IssueDefault import IssueDefault
from VersionControlProvider.IssueMessage import IssueMessage


class Issuer(abc.ABC):

    def __init__(self, state_handler: StateHandler, config_handler: ConfigHandler):
        self.state_handler: StateHandler = state_handler
        self.config_handler: ConfigHandler = config_handler
        self.__repo = None

    @property
    def repo(self) -> Optional[Repo]:
        return self.repo

    def with_repo(self, v: Repo) -> Issuer:
        self.__repo = v
        return self

    @abc.abstractmethod
    def create(self, default_issue: Optional[IssueDefault]) -> Issue:
        pass

    @abc.abstractmethod
    def read_issue_by_number(self, number: int) -> Issue:
        pass

    @abc.abstractmethod
    def message_builder(self, message: str, issue: Optional[Issue] = None) -> IssueMessage:
        pass

    @abc.abstractmethod
    def issue_builder(self) -> Issue:
        pass

    @abc.abstractmethod
    def comment(self, issue: Issue, text: str) -> Issue:
        pass

    @abc.abstractmethod
    def has_repo(self) -> bool:
        pass
