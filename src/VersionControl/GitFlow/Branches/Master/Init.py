from pathlib import Path
from subprocess import PIPE, Popen, STDOUT
import os
import shutil
from FlexioFlow.StateHandler import StateHandler


class Init:
    def __init__(self, state_handler:StateHandler):
        self.__state_handler: StateHandler = state_handler

    def process(self):
        print(self.__state_handler.state.to_dict())
        # workdir: Path = Path('/tmp/flexio_flow_tests')
        # root_path, stderr = Popen(["pwd"], stdout=PIPE).communicate()
        # shutil.rmtree(workdir, True)
        # workdir.mkdir()
        # print(root_path.strip())
        #
        # os.chdir(workdir.as_posix())
        # # subprocess.Popen(["cd", workdir.as_posix()])
        #
        # Popen(["git", "flow", "init", "-f", "-d"]).communicate()
        #
        # Popen(["git", "checkout", "develop"]).communicate()
        # Popen(["git", "pull", "origin", "develop"]).communicate()
        # Popen(["git", "checkout", "-"]).communicate()
        # Popen(["git", "checkout", "master"]).communicate()
        # Popen(["git", "pull", "origin", "master"]).communicate()
        # # get current version
        # Popen(["git", "checkout", "develop"]).communicate()
        #
        # patched_version = '1.2.3'
        #
        # Popen(["git", "flow", "hotfix", "start", patched_version]).communicate()
        # # write file version
        # Popen(["git", "commit", "-am", ''.join(["'Start hotfix : ", patched_version, "'"])]).communicate()
        # Popen(["git", "push"]).communicate()
        # Popen(["pwd"])
        # os.chdir(root_path.strip())
        # Popen(["pwd"])
