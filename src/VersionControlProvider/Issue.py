from __future__ import annotations

from typing import List, Dict


class Issue:
    PREFIX: str = '#'
    number: int
    title: str
    body: str
    milestone: int
    state
    labels: List[str]
    assignees: List[str]

    def __init__(self):
        self.assignees= []
        self.labels= []

    def get_ref(self) -> str:
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
        if self.body:
            issue['body'] = self.body
        if len(self.labels):
            issue['labels'] = self.labels
        if len(self.assignees):
            issue['assignees'] = self.assignees
        return issue
