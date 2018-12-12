import os
import shutil
from pathlib import Path
from subprocess import Popen

from FlexioFlow.Level import Level
from FlexioFlow.State import State
from FlexioFlow.Version import Version
from Schemes.Schemes import Schemes
from VersionControl.GitFlow.GitFlow import GitFlow
from VersionControl.Branches import Branches


class TestGitFlowHelper:
    REPO_URL: str = 'git@github.com:flexiooss/flexio-flow-punching-ball.git'
    DIR_PATH_TEST: Path = Path('/tmp/test_flexioflow')
    TAG_INIT: str = 'init'

    @classmethod
    def mount_workdir_and_clone(cls):
        cls.DIR_PATH_TEST.mkdir()
        Popen(['git', 'clone', cls.REPO_URL, '.'], cwd=cls.DIR_PATH_TEST.as_posix()).communicate()

    @classmethod
    def clean_workdir(cls):
        shutil.rmtree(cls.DIR_PATH_TEST, True)

    @classmethod
    def clean_remote_repo(cls, version: Version = Version(0, 0, 0)):
        os.chdir(cls.DIR_PATH_TEST.as_posix())
        Popen(['git', 'checkout', Branches.MASTER.value], cwd=cls.DIR_PATH_TEST.as_posix()).communicate()
        Popen(['git', 'reset', '--hard', cls.TAG_INIT], cwd=cls.DIR_PATH_TEST.as_posix()).communicate()
        Popen(['git', 'push', '--force', GitFlow.REMOTE, Branches.MASTER.value],
              cwd=cls.DIR_PATH_TEST.as_posix()).communicate()
        Popen(['git', 'push', GitFlow.REMOTE, '--delete', Branches.DEVELOP.value],
              cwd=cls.DIR_PATH_TEST.as_posix()).communicate()
        Popen(['git', 'push', GitFlow.REMOTE, '--delete', str(version)], cwd=cls.DIR_PATH_TEST.as_posix()).communicate()
        Popen(['git', 'push', GitFlow.REMOTE, '--delete', '-'.join([str(version.next_minor()), Level.DEV.value])
               ], cwd=cls.DIR_PATH_TEST.as_posix()).communicate()

    @staticmethod
    def fake_state(version: str = '0.0.0') -> State:
        state: State = State()
        state.version = Version.from_str(version)
        state.schemes = [Schemes.PACKAGE]
        state.level = Level.STABLE
        return state
