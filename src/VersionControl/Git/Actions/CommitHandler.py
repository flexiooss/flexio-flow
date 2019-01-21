from __future__ import annotations

from FlexioFlow.StateHandler import StateHandler
from VersionControl.Git.GitCmd import GitCmd
from VersionControl.CommitHandler import CommitHandler as AbstractCommitHandler


class CommitHandler(AbstractCommitHandler):

    def __init__(self, state_handler: StateHandler):
        super().__init__(state_handler)
        self.__git: GitCmd = GitCmd(self.state_handler)

    def do_commit(self) -> CommitHandler:
        self.__git.commit(self.commit.message)
        return self

    def push(self) -> CommitHandler:
        self.__git.try_to_push()
        return self

    def can_commit(self) -> bool:
        return self.__git.can_commit()
