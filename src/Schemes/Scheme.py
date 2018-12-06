from __future__ import annotations
import abc
from typing import Type, List, NewType
from FlexioFlow.State import State
from Schemes.Dependencies import Dependencies


class Scheme:

    def __init__(self, dir_path: str, state: State):
        self.dir_path: str = dir_path
        self.state: State = state

    @abc.abstractmethod
    def set_version(self) -> Type[Scheme]:
        pass

    @abc.abstractmethod
    def release_plan(self) -> Dependencies:
        pass
