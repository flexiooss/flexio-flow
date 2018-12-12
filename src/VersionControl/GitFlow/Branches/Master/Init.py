from __future__ import annotations

from pathlib import Path
from subprocess import PIPE, Popen
import os
import shutil

from FlexioFlow.Level import Level
from FlexioFlow.StateHandler import StateHandler
from Schemes.UpdateSchemeVersion import UpdateSchemeVersion


class Init:
    def __init__(self, state_handler: StateHandler):
        self.__state_handler: StateHandler = state_handler

    def __init_gitflow(self) -> Init:
        Popen(["git", "flow", "init", "-f", "-d"]).communicate()
        return self

    def __init_master(self) -> Init:
        Popen(["git", "checkout", "master"]).communicate()
        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)
        version: str = str(self.__state_handler.state.version)

        Popen(['git', 'add', '.']).communicate()
        Popen(["git", "commit", "-am",
               ''.join(["'Init master : ", version, "'"])]).communicate()

        Popen(["git", "tag", "-a", version, "-m",
               "'" + version + "'"]).communicate()
        Popen(["git", "push", "--set-upstream", "origin", "master"]).communicate()
        print('Init master at : ' + version)
        Popen(["git", "push", "origin", version]).communicate()
        print('Tag master at : ' + version)
        return self

    def __init_develop(self) -> Init:
        self.__state_handler.state.next_dev_release()
        Popen(["git", "checkout", "develop"]).communicate()
        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)

        version: str = '-'.join([str(self.__state_handler.state.version), Level.DEV.value])

        Popen(['git', 'add', '.']).communicate()

        Popen(["git", "commit", "-am",
               ''.join(["'Init develop : ", version, "'"])]).communicate()
        Popen(["git", "tag", "-a", version, "-m",
               "'" + version + "'"]).communicate()
        Popen(["git", "push", "--set-upstream", "origin", "develop"]).communicate()
        print('Init develop at : ' + version)
        Popen(["git", "push", "origin", version]).communicate()
        print('Tag master at : ' + version)

        return self

    def process(self):
        root_path, stderr = Popen(["pwd"], stdout=PIPE).communicate()

        os.chdir(self.__state_handler.dir_path.as_posix())

        self.__init_gitflow().__init_master().__init_develop()

        os.chdir(root_path.strip())
