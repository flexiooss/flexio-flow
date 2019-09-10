from __future__ import annotations
import abc
from typing import Type, List
from FlexioFlow.StateHandler import StateHandler
from PoomCiDependency.Module import Module
from Schemes.Dependencies import Dependencies


class Scheme(abc.ABC):
    DEV_SUFFIX: str

    def __init__(self, state_handler: StateHandler):
        self.state_handler: StateHandler = state_handler

    @abc.abstractmethod
    def set_version(self) -> Type[Scheme]:
        pass

    @abc.abstractmethod
    def release_precheck(self) -> Dependencies:
        pass

    @abc.abstractmethod
    def get_version(self) -> str:
        pass

    @abc.abstractmethod
    def get_poom_ci_dependencies(self) -> List[Module]:
        pass

    @abc.abstractmethod
    def get_poom_ci_produces(self) -> List[Module]:
        pass
