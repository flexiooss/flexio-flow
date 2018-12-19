from __future__ import annotations
import abc
from typing import Type, Optional

from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Github.Repo import Repo


class Issuer(abc.ABC):

    def __init__(self, config_handler: ConfigHandler):
        self.config_handler: ConfigHandler = config_handler
        self.repo = None

    @property
    def repo(self) -> Optional[Repo]:
        return self.repo

    @repo.setter
    def repo(self, v: Repo):
        self.repo = v

    def with_repo(self, v: Repo) -> Issuer:
        self.repo = v
        return self

    @abc.abstractmethod
    def process(self) -> str:
        pass
