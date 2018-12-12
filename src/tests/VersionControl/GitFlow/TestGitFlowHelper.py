import shutil
from pathlib import Path
from FlexioFlow.Level import Level
from FlexioFlow.State import State
from FlexioFlow.Version import Version
from Schemes.Schemes import Schemes
from VersionControl.GitFlow.GitCmd import GitCmd
from VersionControl.Branches import Branches


class TestGitFlowHelper:
    REPO_URL: str = 'git@github.com:flexiooss/flexio-flow-punching-ball.git'
    DIR_PATH_TEST: Path = Path('/tmp/test_flexioflow')
    TAG_INIT: str = 'init'

    @classmethod
    def mount_workdir_and_clone(cls):
        cls.DIR_PATH_TEST.mkdir()
        git: GitCmd = GitCmd(cls.DIR_PATH_TEST)
        git.clone(cls.REPO_URL)

    @classmethod
    def clean_workdir(cls):
        shutil.rmtree(cls.DIR_PATH_TEST, True)

    @classmethod
    def clean_remote_repo(cls, version: Version = Version(0, 0, 0)):
        git: GitCmd = GitCmd(cls.DIR_PATH_TEST)
        git.checkout(Branches.MASTER.value).reset_tot_tag(cls.TAG_INIT) \
            .push_force() \
            .delete_branch(
            Branches.DEVELOP.value) \
            .delete_tag(str(version)) \
            .delete_tag(
            '-'.join([str(version.next_minor()), Level.DEV.value]))

    @staticmethod
    def fake_state(version: str = '0.0.0') -> State:
        state: State = State()
        state.version = Version.from_str(version)
        state.schemes = [Schemes.PACKAGE]
        state.level = Level.STABLE
        return state
