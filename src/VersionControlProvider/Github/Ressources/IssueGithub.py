from __future__ import annotations

from typing import List, Dict, Optional, Type

from VersionControlProvider.Issue import Issue
from VersionControlProvider.IssueState import IssueState


class IssueGithub(Issue):

    def with_number(self, number: int) -> IssueGithub:
        self.number = number
        return self

    def get_ref(self) -> str:
        if self.number is None:
            raise ValueError('Issue should have a number')
        return '{prefix!s}{number!s}'.format(prefix=self.PREFIX, number=self.number)

    def assign(self, user: str) -> IssueGithub:
        if user not in self.assignees:
            self.assignees.append(user)
        return self

    def label(self, label: str) -> IssueGithub:
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
