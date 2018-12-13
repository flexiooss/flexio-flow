from __future__ import annotations
import abc
from typing import Type
from FlexioFlow.StateHandler import StateHandler
from Schemes.Dependencies import Dependencies


class Scheme(abc.ABC):

    def __init__(self, state_handler: StateHandler):
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

    @abc.abstractmethod
    def get_version(self) -> str:
        pass
