from __future__ import annotations
import yaml
import os
from FlexioFlow.State import State
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from FlexioFlow.Version import Version
from Exceptions.FileNotExistError import FileNotExistError


class StateHandler:
    FILE_NAME = 'flexio-flow.yml'
    __state: State

    def __init__(self, dir_path: str):
        self.dir_path: str = dir_path
        self.__state = State()

    @property
    def state(self) -> State:
        return self.__state

    @state.setter
    def state(self, v: State):
        self.__state = v

    def file_exists(self) -> bool:
        return os.path.isfile(self.file_path())

    def load_file_config(self) -> StateHandler:
        if not os.path.isfile(self.file_path()):
            raise FileNotExistError(self.file_path(), 'Flexio Flow not initialized try : flexio-flow init')
        data = yaml.load(open(self.file_path(), 'r'))

        self.__state.version = Version.from_str(data['version'])
        self.__state.scheme = Schemes.list_from_value(data['scheme'])
        self.__state.level = Level(data['level'])

        return self

    def write_file(self) -> str:
        stream = open(self.file_path(), 'w')
        yaml.dump(self.state.to_dict(), stream)
        return yaml.dump(self.state.to_dict())

    def file_path(self) -> str:
        return self.dir_path + self.FILE_NAME
