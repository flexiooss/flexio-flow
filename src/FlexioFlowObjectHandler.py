import yaml
import os
from FlexioFlowValueObject import FlexioFlowValueObject


class FlexioFlowObjectHandler:
    state: FlexioFlowValueObject
    file_path: str
    FILE_NAME = 'flexio-flow.yml'

    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise ValueError(file_path + ' : File not exists')
        self.file_path = file_path

    @property
    def state(self) -> FlexioFlowValueObject:
        return self.__state

    @state.setter
    def state(self, v: FlexioFlowValueObject):
        self.__state = v

    def loadFileConfig(self):
        data = yaml.load(open(self.file_path, 'r'))
        print(data)
        self.__state = 'bibi'
