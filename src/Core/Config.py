from __future__ import annotations
from typing import Dict, Optional

from VersionControlProvider.Flexio.ConfigFlexio import ConfigFlexio
from VersionControlProvider.Github.ConfigGithub import ConfigGithub


class Config:
    __github: Optional[ConfigGithub] = None
    __flexio: Optional[ConfigFlexio] = None

    def with_github(self, github: ConfigGithub) -> Config:
        c: Config = Config()
        c.__github = github
        if self.__flexio is not None:
            c.__flexio = self.__flexio
        return c

    def with_flexio(self, flexio: ConfigFlexio) -> Config:
        c: Config = Config()
        c.__flexio = flexio
        if self.__github is not None:
            c.__github = self.__github
        return c

    @property
    def github(self) -> ConfigGithub:
        return self.__github

    @property
    def flexio(self) -> ConfigFlexio:
        return self.__flexio

    def to_dict(self) -> Dict[str, dict]:
        return {
            'github': self.github.to_dict(),
            'flexio': self.flexio.to_dict()
        }
