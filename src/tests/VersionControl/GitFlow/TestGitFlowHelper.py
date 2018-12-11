import os
import shutil
from pathlib import Path
from subprocess import Popen
from VersionControl.GitFlow.GitFlow import GitFlow
from VersionControl.Branches import Branches


class TestGitFlowHelper:
    REPO_URL: str = 'git@github.com:flexiooss/flexio-flow-punching-ball.git'
    DIR_PATH_TEST: Path = Path('/tmp/test_flexioflow')
    TAG_INIT: str = 'init'

    @classmethod
    def mount_workdir_and_clone(cls):
        cls.DIR_PATH_TEST.mkdir()
        os.chdir(cls.DIR_PATH_TEST.as_posix())
        Popen(['git', 'clone', cls.REPO_URL, '.'])

    @classmethod
    def clean_workdir(cls):
        shutil.rmtree(cls.DIR_PATH_TEST)

    @classmethod
    def clean_remote_repo(cls):
        Popen(['git', 'checkout', Branches.MASTER.value])
        Popen(['git', 'reset', '--hard', cls.TAG_INIT])
        Popen(['git', 'push', '--force', GitFlow.REMOTE, Branches.MASTER.value])
        Popen(['git', 'push', GitFlow.REMOTE, '--delete', Branches.DEVELOP.value])
