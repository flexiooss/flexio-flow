import yaml
import os
import pprint


class FileConfig:
    file_path: str
    FILE_NAME = 'flexio-flow.yml'

    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise ValueError(file_path + ' : File not exists')
        self.file_path = file_path

    def parse(self):
        data = yaml.load(open(self.file_path, 'r'))
        print(data)
