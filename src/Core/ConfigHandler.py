from __future__ import annotations

from typing import Optional

import yaml
from Core.Config import Config
from Exceptions.FileNotExistError import FileNotExistError
from pathlib import Path
import fileinput


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
            raise FileNotExistError(
                self.file_path(),
                'Flexio Flow Core not initialized try : flexio-flow core config'
            )
        f: fileinput = self.file_path().open('r')
        data = yaml.load(f)
        f.close()


        self.__config = Config(user=data['user'], token=data['token'])

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
