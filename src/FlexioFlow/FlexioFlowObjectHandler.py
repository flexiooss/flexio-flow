import yaml
import os
from FlexioFlow.FlexioFlowValueObject import FlexioFlowValueObject
from FlexioFlow.Level import Level
from FlexioFlow.Scheme import Scheme
from utils.EnumUtils import EnumUtils
from typing import Tuple, NewType
import re

version_type = NewType('version', Tuple[int, int, int])


class FlexioFlowObjectHandler:
    __state: FlexioFlowValueObject
    file_path: str
    FILE_NAME = 'flexio-flow.yml'
    __version: version_type

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

    @property
    def version(self) -> version_type:
        return self.__version

    @version.setter
    def version(self, v: version_type):
        if not isinstance(v, version_type):
            raise TypeError('version should be an instance of version_type')
        self.__version = v

    def versionFromStr(self, v: str) -> version_type:
        matches = re.match('^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$', v)
        return (int(matches.groupdict().get('major')),
                int(matches.groupdict().get('minor')),
                int(matches.groupdict().get('patch')))

    def loadFileConfig(self):
        data = yaml.load(open(self.filePath(), 'r'))

        self.__state = FlexioFlowValueObject(
            version=data['version'],
            scheme=EnumUtils(Scheme).list_from_value(data['scheme']),
            level=Level(data['level']))
        print(repr(self.__state.to_dict()))
        print(self.versionFromStr(data['version']))
        self.version = self.versionFromStr(data['version'])

    def filePath(self) -> str:
        return self.file_path + '/' + self.FILE_NAME
