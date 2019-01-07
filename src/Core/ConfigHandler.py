from __future__ import annotations

from typing import Optional

import yaml
from Core.Config import Config
from pathlib import Path
import fileinput

from VersionControlProvider.Flexio.ConfigFlexio import ConfigFlexio
from VersionControlProvider.Github.ConfigGithub import ConfigGithub


class ConfigHandler:
    FILE_NAME: str = 'config.yml'
    __config: Optional[Config]

    def __init__(self, dir_path: Path):
        self.dir_path: Path = dir_path
        self.__config: Optional[Config] = None

    @property
    def config(self) -> Config:
        return self.__config

    @config.setter
    def config(self, v: Config):
        self.__config = v

    def file_exists(self) -> bool:
        return self.file_path().is_file()

    def load_file_config(self) -> ConfigHandler:
        if not self.file_path().is_file():
            raise FileNotFoundError(
                self.file_path(),
                'Flexio Flow Core not initialized try : flexio-flow core config'
            )
        f: fileinput = self.file_path().open('r')
        data: dict = yaml.load(f)
        f.close()

        self.__config = Config().with_github(
            github=ConfigGithub(
                activate=data.get('github', {}).get('activate', False),
                user=data.get('github', {}).get('user', ''),
                token=data.get('github', {}).get('token', '')
            )
        ).with_flexio(flexio=ConfigFlexio(
            activate=data.get('flexio', {}).get('activate', False),
            user_token=data.get('flexio', {}).get('user_token', ''),
            service_token=data.get('flexio', {}).get('service_token', '')
        ))
        return self

    def write_file(self) -> str:
        stream = self.file_path().open('w')
        print(self.__config.to_dict())
        yaml.dump(self.__config.to_dict(), stream, default_flow_style=False)
        stream.close()
        print('write file : ' + self.file_path().as_posix())
        return yaml.dump(self.__config.to_dict(), default_flow_style=False)

    def file_path(self) -> Path:
        return self.dir_path / self.FILE_NAME

    def has_issuer(self) -> bool:
        return self.__config.github.activate is True
