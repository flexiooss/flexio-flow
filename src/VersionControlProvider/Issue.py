from __future__ import annotations

from typing import List, Dict, Optional

from VersionControlProvider.IssueState import IssueState
import abc


class Issue(abc.ABC):
    PREFIX: str = '#'
    number: Optional[int]
    title: Optional[str]
    body: Optional[str]
    milestone: Optional[int]
    state: Optional[IssueState]
    labels: List[str]
    assignees: List[str]

    def __init__(self):
        self.number = None
        self.title = None
        self.body = None
        self.milestone = None
        self.state = None
        self.assignees = []
        self.labels = []

    def with_number(self, number: int) -> Issue:
        self.number = number
        return self

    @abc.abstractmethod
    def get_ref(self) -> str:
        pass

    @abc.abstractmethod
    def __dict__(self):
        pass
