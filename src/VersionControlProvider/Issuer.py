from __future__ import annotations
import abc
from typing import Type, Optional

from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Github.Repo import Repo


class Issuer(abc.ABC):

    def __init__(self, config_handler: ConfigHandler):
        self.config_handler: ConfigHandler = config_handler
        self.__repo = None

    @property
    def repo(self) -> Optional[Repo]:
        return self.repo

    def with_repo(self, v: Repo) -> Issuer:
        self.__repo = v
        return self

    @abc.abstractmethod
    def create(self) -> str:
        pass
