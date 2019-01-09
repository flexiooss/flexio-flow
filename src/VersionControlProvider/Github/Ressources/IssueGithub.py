from __future__ import annotations

from VersionControlProvider.Issue import Issue
from VersionControlProvider.IssueState import IssueState


class IssueGithub(Issue):

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

    @staticmethod
    def from_api_dict(data: dict) -> IssueGithub:
        inst: IssueGithub = IssueGithub()
        inst.number = data.get('number')
        print(data.get('state'))
        inst.state = IssueState.CLOSED if data.get('state') == 'closed' else IssueState.OPEN
        inst.milestone = data.get('milestone')
        inst.assignees = data.get('assignees')
        inst.url = data.get('url')
        return inst

    def __dict__(self):
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
