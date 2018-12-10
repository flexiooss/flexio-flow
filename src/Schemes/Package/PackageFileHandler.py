from __future__ import annotations
import json
import os
from Exceptions.FileNotExistError import FileNotExistError
from FlexioFlow.Version import Version
from Schemes.Dependencies import Dependencies
from Exceptions.HaveDevDependencyException import ReleasePlanException
from typing import Dict
import re


class PackageFileHandler:
    FILE_NAME: str = 'package.json'
    VERSION_KEY: str = 'version'
    DEPENDENCIES_KEY: str = 'dependencies'

    def __init__(self, dir_path: str):
        self.__file_path: str = dir_path + self.FILE_NAME
        self.__data: dict = self.__load_file()

    @property
    def data(self) -> dict:
        return self.__data

    def __load_file(self):
        if not os.path.isfile(self.__file_path):
            raise FileNotExistError(self.__file_path)
        with open(self.__file_path) as json_data:
            d = json.load(json_data)
            return d

    def get_version(self) -> str:
        return self.__data[self.VERSION_KEY]

    def set_version(self, version: Version) -> PackageFileHandler:
        self.__data[self.VERSION_KEY] = str(version)
        return self

    def write(self) -> PackageFileHandler:
        with open(self.__file_path, 'w') as outfile:
            json.dump(self.__data, outfile, indent=2)
        return self

    @staticmethod
    def is_git_dependency(v: str) -> bool:
        return re.match('.*(.git)+.*', v) is not None
