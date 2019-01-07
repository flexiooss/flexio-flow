from __future__ import annotations

from typing import Optional

from VersionControlProvider.Message import Message


class Commit:
    message: Optional[Message]
    id: Optional[str]

    def __init__(self):
        self.message = None

    def with_message(self, message: str) -> Commit:
        self.message = message
        return self
