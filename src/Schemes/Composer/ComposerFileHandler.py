from __future__ import annotations
import json
from pathlib import Path


class ComposerFileHandler:
    FILE_NAME: str = 'composer.json'
    VERSION_KEY: str = 'version'
    DEPENDENCIES_KEY: str = 'require'
    NAME: str = 'name'

    def __init__(self, dir_path: Path):
        self.__file_path: Path = dir_path / self.FILE_NAME
        self.__data: dict = self.__load_file()

    @property
    def data(self) -> dict:
        return self.__data

    def __load_file(self):
        if not self.__file_path.is_file():
            raise FileNotFoundError(self.__file_path)
        with self.__file_path.open() as json_data:
            d = json.load(json_data)
            return d

    def get_version(self) -> str:
        return self.__data[self.VERSION_KEY]

    def set_version(self, version: str) -> ComposerFileHandler:
        self.__data[self.VERSION_KEY] = version
        return self

    def get_name(self) -> str:
        return self.__data[self.NAME]

    def write(self) -> ComposerFileHandler:
        with self.__file_path.open('w') as outfile:
            json.dump(self.__data, outfile, indent=2)
        return self
