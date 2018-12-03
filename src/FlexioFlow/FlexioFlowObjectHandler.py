import yaml
import os
from FlexioFlow.FlexioFlowValueObject import FlexioFlowValueObject
from FlexioFlow.Level import Level
from FlexioFlow.Scheme import Scheme
from utils.EnumUtils import EnumUtils


class FlexioFlowObjectHandler:
    __state: FlexioFlowValueObject
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
        data = yaml.load(open(self.filePath(), 'r'))

        self.__state = FlexioFlowValueObject(
            version=data['version'],
            scheme=EnumUtils(Scheme).list_from_value(data['scheme']),
            level=Level(data['level']))
        print(repr(self.__state.to_dict()))

    def filePath(self) -> str:
        return self.file_path + '/' + self.FILE_NAME
