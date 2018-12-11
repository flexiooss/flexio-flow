from pathlib import Path
from subprocess import PIPE, Popen, STDOUT
import os
import shutil
from FlexioFlow.StateHandler import StateHandler


class Init:
    def __init__(self, state_handler: StateHandler):
        self.__state_handler: StateHandler = state_handler

    def process(self):

        root_path, stderr = Popen(["pwd"], stdout=PIPE).communicate()

        os.chdir(self.__state_handler.dir_path.as_posix())
        Popen(["git", "flow", "init", "-f", "-d"]).communicate()

        Popen(["git", "checkout", "master"]).communicate()
        self.__state_handler.write_file()
        Popen(["git", "commit", "-am",
               ''.join(["'Init master : ", str(self.__state_handler.state.version), "'"])]).communicate()

        Popen(["git", "tag", "-a", str(self.__state_handler.state.version), "-m",
               "'" + str(self.__state_handler.state.version) + "'"]).communicate()
        Popen(["git", "push", "--set-upstream", "origin", "master"]).communicate()
        print('Init master at : ' + str(self.__state_handler.state.version))
        Popen(["git", "push", "origin", str(self.__state_handler.state.version)]).communicate()
        print('Tag master at : ' + str(self.__state_handler.state.version))

        self.__state_handler.state.next_dev_release()
        Popen(["git", "checkout", "develop"]).communicate()
        self.__state_handler.write_file()
        Popen(["git", "commit", "-am",
               ''.join(["'Init develop : ", str(self.__state_handler.state.version), "'"])]).communicate()
        Popen(["git", "push", "--set-upstream", "origin", "develop"]).communicate()
        print('Init develop at : ' + str(self.__state_handler.state.version))

        os.chdir(root_path.strip())
