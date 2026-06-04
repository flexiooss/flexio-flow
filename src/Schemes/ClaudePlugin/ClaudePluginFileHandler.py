from __future__ import annotations
import json
from pathlib import Path


class ClaudePluginFileHandler:
    VERSION_KEY: str = 'version'
    NAME: str = 'name'

    def __init__(self, file_path: Path):
        self.__file_path: Path = file_path
        self.__data: dict = self.__load_file()

    @property
    def data(self) -> dict:
        return self.__data

    def __load_file(self) -> dict:
        if not self.__file_path.is_file():
            raise FileNotFoundError(self.__file_path)
        with self.__file_path.open() as json_data:
            return json.load(json_data)

    def get_version(self) -> str:
        return self.__data[self.VERSION_KEY]

    def set_version(self, version: str) -> ClaudePluginFileHandler:
        self.__data[self.VERSION_KEY] = version
        return self

    def get_name(self) -> str:
        return self.__data[self.NAME]

    def write(self) -> ClaudePluginFileHandler:
        with self.__file_path.open('w') as outfile:
            json.dump(self.__data, outfile, indent=2)
            outfile.write("\n")
        return self
