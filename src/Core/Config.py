from __future__ import annotations
from typing import Dict

from VersionControlProvider.Github.ConfigGithub import ConfigGithub


class Config:

    def __init__(self, github: ConfigGithub) -> None:
        self.__github: ConfigGithub = github

    def with_github(self, github: ConfigGithub) -> Config:
        return Config(github)

    @property
    def github(self) -> ConfigGithub:
        return self.__github

    def to_dict(self) -> Dict[str, dict]:
        return {
            'github': self.github.to_dict()
        }
