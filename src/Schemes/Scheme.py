from __future__ import annotations
import abc
from typing import Type, List, NewType

dependencies = NewType('dependencies', List[str])


class Scheme:

    def __init__(self, dir_path: str):
        self.dir_path: str = dir_path

    @abc.abstractmethod
    def set_version(self) -> Type[Scheme]:
        pass

    @abc.abstractmethod
    def release_plan(self) -> dependencies:
        pass
