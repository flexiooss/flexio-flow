from __future__ import annotations
import yaml
import os
from FlexioFlow.State import State
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from FlexioFlow.Version import Version


class StateHandler:
    FILE_NAME = 'flexio-flow.yml'
    __state: State

    def __init__(self, dir_path: str):
        if not os.path.exists(dir_path):
            raise ValueError(dir_path + ' : File not exists')
        self.dir_path: str = dir_path.rstrip('/') + '/'

    @property
    def state(self) -> State:
        return self.__state

    @state.setter
    def state(self, v: State):
        self.__state = v

    def load_file_config(self) -> StateHandler:
        data = yaml.load(open(self.file_path(), 'r'))

        self.__state = State(
            version=Version.from_str(data['version']),
            scheme=Schemes.list_from_value(data['scheme']),
            level=Level(data['level']))
        return self

    def file_path(self) -> str:
        return self.dir_path + self.FILE_NAME
