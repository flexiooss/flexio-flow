from __future__ import annotations

from VersionControlProvider.Issue import Issue
from VersionControlProvider.IssueState import IssueState


class IssueDefault(Issue):

    def get_ref(self) -> str:
        if self.number is None:
            raise ValueError('Issue should have a number')
        return '{prefix!s}{number!s}'.format(prefix=self.PREFIX, number=self.number)

    def __dict__(self):
        issue: dict = {
            'title': self.title
        }
        if self.body is not None:
            issue['body'] = self.body
        if self.milestone is not None:
            issue['milestone'] = self.milestone
        if self.url is not None:
            issue['url'] = self.url
        if self.state is not None:
            issue['state'] = self.state.value
        if len(self.labels):
            issue['labels'] = self.labels
        if len(self.assignees):
            issue['assignees'] = self.assignees

        return issue
