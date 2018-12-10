from __future__ import annotations
import abc
from typing import Type, List, NewType
from FlexioFlow.State import State
from Schemes.Dependencies import Dependencies
from pathlib import Path

class Scheme:

    def __init__(self, dir_path: Path, state: State):
        self.dir_path: Path = dir_path
        self.state: State = state

    @property
    @abc.abstractmethod
    def DEV_SUFFIX(self) -> str:
        pass

    @abc.abstractmethod
    def set_version(self) -> Type[Scheme]:
        pass

    @abc.abstractmethod
    def release_precheck(self) -> Dependencies:
        pass
