import json
import os


class PackageFileHandler:
    FILE_NAME: str = 'package.json'
    VERSION_KEY: str = 'version'

    def __init__(self, dir_path: str):
        self.__file_path: str = dir_path + self.FILE_NAME

    def __load_file(self):
        if not os.path.exists(self.__file_path):
            raise ValueError(self.__file_path + ' : File not exists')
        with open(self.__file_path) as json_data:
            d = json.load(json_data)
            print(d)
