from __future__ import annotations
import abc
from typing import Type, Optional

from VersionControlProvider.IssueState import IssueState


class Topicer(abc.ABC):
    number: int
    title: str
    state: Optional[IssueState]
    description: Optional[str]
