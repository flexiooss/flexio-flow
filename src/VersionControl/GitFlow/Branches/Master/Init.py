from pathlib import Path
from subprocess import PIPE, Popen, STDOUT
import os
import shutil
from FlexioFlow.StateHandler import StateHandler


class Init:
    def __init__(self, state_handler: StateHandler):
        self.__state_handler: StateHandler = state_handler

    def process(self):
        print(self.__state_handler.state.to_dict())
        # workdir: Path = Path('/tmp/flexio_flow_tests')
        root_path, stderr = Popen(["pwd"], stdout=PIPE).communicate()
        # shutil.rmtree(workdir, True)
        # workdir.mkdir()
        # print(root_path.strip())
        #
        os.chdir(self.__state_handler.dir_path.as_posix())
        Popen(["git", "flow", "init", "-f", "-d"]).communicate()
        Popen(["git", "checkout", "master"]).communicate()
        self.__state_handler.write_file()
        Popen(["git", "commit", "-am", ''.join(["'Init master : ", str(self.__state_handler.state.version), "'"])]).communicate()
        Popen(["git", "push", "--set-upstream", "origin", "master"]).communicate()
        #
        Popen(["git", "checkout", "develop"]).communicate()
        # Popen(["git", "pull", "origin", "develop"]).communicate()
        # Popen(["git", "checkout", "-"]).communicate()
        # Popen(["git", "pull", "origin", "master"]).communicate()
        # # get current version
        # Popen(["git", "checkout", "develop"]).communicate()
        #
        # patched_version = '1.2.3'
        #
        # Popen(["git", "flow", "hotfix", "start", patched_version]).communicate()
        # # write file version
        # Popen(["git", "push"]).communicate()
        # Popen(["pwd"])
        os.chdir(root_path.strip())
        # Popen(["pwd"])
