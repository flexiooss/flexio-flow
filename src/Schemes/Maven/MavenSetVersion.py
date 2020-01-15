from __future__ import annotations
import sys

from subprocess import Popen

from FlexioFlow.StateHandler import StateHandler


class MavenSetVersion:
    __state_handler: StateHandler
    target_version: str

    def __init__(self, state_handler: StateHandler, target_version: str):
        self.__state_handler: StateHandler = state_handler
        self.target_version: str = target_version

    def set(self):
        p1 = Popen(
            ['mvn', 'versions:set', '-DnewVersion=' + self.target_version, '-U'],
            cwd=self.__state_handler.dir_path.as_posix()
        )
        p1.wait()

        if p1.returncode is not 0:
            print('something went wrong while setting version, trying to rollback')
            status = Popen(
                ['mvn', 'versions:rollback'],
                cwd=self.__state_handler.dir_path.as_posix()
            ).wait()

            status = Popen(
                ['mvn', 'versions:commit'],
                cwd=self.__state_handler.dir_path.as_posix()
            ).wait()

            sys.stderr.write("Command terminated with wrong status code: " + str(p1.returncode) + "\n")
            sys.exit(p1.returncode)
