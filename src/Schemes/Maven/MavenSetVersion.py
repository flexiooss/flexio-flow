from __future__ import annotations

from subprocess import Popen

from FlexioFlow.StateHandler import StateHandler


class MavenSetVersion:
    __state_handler: StateHandler
    target_version: str

    def __init__(self, state_handler: StateHandler, target_version: str):
        self.__state_handler: StateHandler = state_handler
        self.target_version: str = target_version

    def set(self):
        status = Popen(
            ['mvn', 'versions:set', '-DnewVersion=' + self.target_version],
            cwd=self.__state_handler.dir_path.as_posix()
        ).wait()

        if status is not 0:
            print('something went wrong while setting version, trying to rollback')
            status = Popen(
                ['mvn', 'versions:rollback'],
                cwd=self.__state_handler.dir_path.as_posix()
            ).wait()

        status = Popen(
            ['mvn', 'versions:commit'],
            cwd=self.__state_handler.dir_path.as_posix()
        ).wait()
