from __future__ import annotations

from typing import List, Dict, Optional

from VersionControlProvider.IssueState import IssueState


class Milestone:
    number: Optional[int]
    title: Optional[str]
    description: Optional[str]
    state: Optional[IssueState]

    def __init__(self):
        self.number = None
        self.title = None
        self.description = None
        self.state = None

    def with_number(self, number: int) -> Milestone:
        self.number = number
        return self

    def __dict__(self) -> dict:
        milestone: dict = {
            'title': self.title
        }
        if self.description is not None:
            milestone['description'] = self.description
        if self.state is not None:
            milestone['state'] = self.state.value

        return milestone
