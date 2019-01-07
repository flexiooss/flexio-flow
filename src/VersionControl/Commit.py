from __future__ import annotations

from typing import Optional

from VersionControlProvider.IssueMessage import IssueMessage


class Commit:
    message: Optional[IssueMessage]
    id: Optional[str]

    def __init__(self):
        self.message = None

    def with_message(self, message: str) -> Commit:
        self.message = message
        return self
