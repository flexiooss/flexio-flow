from __future__ import annotations

from typing import List, Dict, Optional

from VersionControlProvider.IssueState import IssueState


class Issue:
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

    def get_ref(self) -> str:
        if self.number is None:
            raise ValueError('Issue should have a number')
        return '{prefix!s}{number!s}'.format(prefix=self.PREFIX, number=self.number)

    def assign(self, user: str) -> Issue:
        if user not in self.assignees:
            self.assignees.append(user)
        return self

    def label(self, label: str) -> Issue:
        if label not in self.labels:
            self.labels.append(label)
        return self

    def __dict__(self) -> dict:
        issue: dict = {
            'title': self.title
        }
        if self.body is not None:
            issue['body'] = self.body
        if self.milestone is not None:
            issue['milestone'] = self.milestone
        if self.state is not None:
            issue['state'] = self.state.value
        if len(self.labels):
            issue['labels'] = self.labels
        if len(self.assignees):
            issue['assignees'] = self.assignees
        return issue
