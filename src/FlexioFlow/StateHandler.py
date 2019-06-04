from __future__ import annotations

from typing import Optional

import yaml
from FlexioFlow.State import State
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from FlexioFlow.Version import Version
from pathlib import Path
import fileinput

from VersionControlProvider.DefaultTopic import DefaultTopic


class StateHandler:
    FILE_NAME: str = 'flexio-flow.yml'
    __state: State

    def __init__(self, dir_path: Path):
        self.dir_path: Path = dir_path
        self.reset_state()

    @property
    def state(self) -> State:
        return self.__state

    @state.setter
    def state(self, v: State):
        self.__state = v

    def reset_state(self):
        self.__state = State()

    def file_exists(self) -> bool:
        return self.file_path().is_file()

    def load_file_config(self) -> StateHandler:
        if not self.file_path().is_file():
            raise FileNotFoundError(self.file_path(), 'Flexio Flow not initialized try : flexio-flow init')
        f: fileinput = self.file_path().open('r')
        data = yaml.load(f)
        f.close()

        self.__state.version = Version.from_str(data['version'])
        self.__state.schemes = Schemes.list_from_value(data['schemes'])
        self.__state.level = Level(data['level'])
        self.__state.topic = DefaultTopic().with_number(data.get('topic'))

        return self

    def write_file(self) -> str:
        stream = self.file_path().open('w')
        yaml.dump(self.state.to_dict(), stream)
        stream.close()
        print('Write file state : ' + self.file_path().as_posix())
        return yaml.dump(self.state.to_dict())

    def file_path(self) -> Path:
        return self.dir_path / self.FILE_NAME

    def next_major(self) -> Version:
        self.__state.version = self.__state.version.next_major()
        return self.__state.version

    def next_minor(self) -> Version:
        self.__state.version = self.__state.version.next_minor()
        return self.__state.version

    def next_patch(self) -> Version:
        self.__state.version = self.__state.version.next_patch()
        return self.__state.version

    def reset_patch(self) -> Version:
        self.__state.version = self.__state.version.reset_patch()
        return self.__state.version

    def reset_minor(self) -> Version:
        self.__state.version = self.__state.version.reset_minor()
        return self.__state.version

    def reset_major(self) -> Version:
        self.__state.version = self.__state.version.reset_major()
        return self.__state.version

    def is_dev(self) -> bool:
        return self.__state.level is Level.DEV

    def next_dev_patch(self) -> Version:
        self.__state.version = self.__state.next_dev_patch()
        return self.__state.version

    def get_next_patch_version(self) -> Version:
        return self.__state.version.next_patch()

    def next_dev_minor(self) -> Version:
        self.__state.version = self.__state.next_dev_minor()
        return self.__state.version

    def version_as_str(self) -> str:
        return str(self.__state.version)

    def set_dev(self) -> StateHandler:
        self.__state = self.__state.set_dev()
        return self

    def set_stable(self) -> StateHandler:
        self.__state = self.__state.set_stable()
        return self

    def first_scheme(self) -> Optional[Schemes]:
        if len(self.state.schemes) > 0:
            return self.state.schemes[0]
        else:
            return None

    def has_default_topic(self) -> bool:
        return self.__state.topic.number is not None

    def default_topic(self) -> DefaultTopic:
        return self.__state.topic
