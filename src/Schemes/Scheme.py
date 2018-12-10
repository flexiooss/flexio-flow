from __future__ import annotations
import abc
from typing import Type, List, NewType
from FlexioFlow.StateHandler import StateHandler
from Schemes.Dependencies import Dependencies
from pathlib import Path


class Scheme(abc.ABC):

    def __init__(self,  state_handler: StateHandler):
        self.state_handler: StateHandler = state_handler

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
