from __future__ import annotations
import abc
from typing import Optional

from FlexioFlow.StateHandler import StateHandler
from VersionControl import Commit


class CommitHandler(abc.ABC):
    commit: Optional[Commit]
    state_handler: StateHandler

    def __init__(self, state_handler: StateHandler):
        self.state_handler: StateHandler = state_handler
        self.commit: Optional[Commit] = None

    def with_commit(self, commit: Optional[Commit]) -> CommitHandler:
        self.commit = commit
        return self

    @abc.abstractmethod
    def do_commit(self) -> CommitHandler:
        pass

    @abc.abstractmethod
    def push(self) -> CommitHandler:
        pass

    @abc.abstractmethod
    def can_commit(self) -> bool:
        pass
