from __future__ import annotations
import abc
from typing import Optional

from VersionControlProvider.IssueState import IssueState


class Topic(abc.ABC):
    number: int
    title: str
    state: Optional[IssueState]
    body: Optional[str]

    def __init__(self):
        self.number = None
        self.title = None
        self.body = None
        self.state = None

    def with_number(self, number: int) -> Topic:
        self.number = number
        return self

    @abc.abstractmethod
    def __dict__(self):
        pass

    @abc.abstractmethod
    def url(self) -> str:
        pass

