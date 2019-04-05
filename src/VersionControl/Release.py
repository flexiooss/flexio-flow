from __future__ import annotations
import abc

from FlexioFlow.StateHandler import StateHandler
from VersionControl.Branch import Branch


class Release(Branch, abc.ABC):
    is_major: bool

    def __init__(self, state_handler: StateHandler) -> None:
        super(Release, self).__init__(state_handler)
        self.is_major = False

    def with_major(self, is_major: bool) -> Release:
        self.is_major = is_major
        return self
