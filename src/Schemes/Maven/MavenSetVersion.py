from __future__ import annotations

from subprocess import Popen

from pathlib import Path


class MavenSetVersion:
    dir_path: str
    targetVersion: str

    def __init__(self, dir_path: Path):
        self.dir_path = dir_path

    def set(self):
        status = Popen(
            ['mvn', 'versions:set', '-DnewVersion=' + self.targetVersion],
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
