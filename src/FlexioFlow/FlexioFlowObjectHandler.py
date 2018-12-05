from __future__ import annotations
import yaml
import os
from FlexioFlow.FlexioFlowValueObject import FlexioFlowValueObject
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from FlexioFlow.Version import Version
from utils.EnumUtils import EnumUtils


class FlexioFlowObjectHandler:
    __state: FlexioFlowValueObject
    FILE_NAME = 'flexio-flow.yml'
    __version: Version

    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise ValueError(file_path + ' : File not exists')
        self.file_path: str = file_path

    @property
    def state(self) -> FlexioFlowValueObject:
        return self.__state

    @state.setter
    def state(self, v: FlexioFlowValueObject):
        self.__state = v

    @property
    def version(self) -> Version:
        return self.__version

    @version.setter
    def version(self, v: Version):
        if not isinstance(v, Version):
            raise TypeError('version should be an instance of FlexioFlow.Version')
        self.__version = v

    def loadFileConfig(self) -> FlexioFlowObjectHandler:
        data = yaml.load(open(self.filePath(), 'r'))

        self.__state = FlexioFlowValueObject(
            version=Version.from_str(data['version']),
            scheme=EnumUtils(Schemes).list_from_value(data['scheme']),
            level=Level(data['level']))
        return self

    def filePath(self) -> str:
        return self.file_path + '/' + self.FILE_NAME
