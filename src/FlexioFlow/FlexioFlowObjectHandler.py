from __future__ import annotations
import yaml
import os
from FlexioFlow.FlexioFlowValueObject import FlexioFlowValueObject
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from FlexioFlow.Version import Version
from utils.EnumUtils import EnumUtils


class FlexioFlowObjectHandler:
    FILE_NAME = 'flexio-flow.yml'
    __state: FlexioFlowValueObject
    __version: Version

    def __init__(self, dir_path: str):
        if not os.path.exists(dir_path):
            raise ValueError(dir_path + ' : File not exists')
        self.dir_path: str = dir_path.rstrip('/') + '/'

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

    def load_file_config(self) -> FlexioFlowObjectHandler:
        data = yaml.load(open(self.file_path(), 'r'))

        self.__state = FlexioFlowValueObject(
            version=Version.from_str(data['version']),
            scheme=Schemes.list_from_value(data['scheme']),
            level=Level(data['level']))
        return self

    def file_path(self) -> str:
        return self.dir_path + self.FILE_NAME
