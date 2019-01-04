import shutil
from pathlib import Path

from Core.Config import Config
from Core.ConfigHandler import ConfigHandler
from Branches.Actions.Actions import Actions
from FlexioFlow.Level import Level
from FlexioFlow.State import State
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.Version import Version
from Schemes.Schemes import Schemes
from VersionControl.GitFlow.GitCmd import GitCmd
from Branches.Branches import Branches
from VersionControl.GitFlow.GitFlow import GitFlow
from VersionControlProvider.Github.ConfigGithub import ConfigGithub
from VersionControlProvider.Github.Github import Github
from VersionControlProvider.Github.Repo import Repo
from tests.VersionControlProvider.Github.api___secret import TOKEN_TEST, USER


class TestGitFlowHelper:
    REPO_URL: str = 'git@github.com:flexiooss/flexio-flow-punching-ball.git'
    DIR_PATH_TEST: Path = Path('/tmp/test_flexioflow')
    TAG_INIT: str = 'init'

    @classmethod
    def mount_workdir_and_clone(cls):
        cls.DIR_PATH_TEST.mkdir()
        git: GitCmd = GitCmd(state_handler=StateHandler(TestGitFlowHelper.DIR_PATH_TEST))
        git.clone(cls.REPO_URL)

    @classmethod
    def clean_workdir(cls):
        shutil.rmtree(cls.DIR_PATH_TEST, True)

    @classmethod
    def clean_remote_repo(cls, version: Version = Version(0, 0, 0)):
        git: GitCmd = GitCmd(state_handler=StateHandler(TestGitFlowHelper.DIR_PATH_TEST))
        git.checkout(Branches.MASTER).reset_to_tag(cls.TAG_INIT) \
            .push_force() \
            .delete_branch_from_name(Branches.DEVELOP.value, remote=True) \
            .delete_tag(str(version), remote=True) \
            .delete_tag('-'.join([str(version.next_minor()), Level.DEV.value]), remote=True)

    @staticmethod
    def fake_state(version: str = '0.0.0') -> State:
        state: State = State()
        state.version = Version.from_str(version)
        state.schemes = [Schemes.PACKAGE]
        state.level = Level.STABLE
        return state

    @classmethod
    def init_repo(cls, version: str) -> StateHandler:
        cls.clean_workdir()
        cls.mount_workdir_and_clone()
        state_handler: StateHandler = StateHandler(cls.DIR_PATH_TEST)
        state_handler.state = cls.fake_state(version)
        GitFlow(state_handler).build_branch(Branches.MASTER).with_action(Actions.INIT).process()
        return state_handler

    @classmethod
    def setup_config_handler(cls) -> ConfigHandler:
        config_handler: ConfigHandler = ConfigHandler(cls.DIR_PATH_TEST)
        config_handler.config = Config(ConfigGithub(
            activate=True,
            user=USER,
            token=TOKEN_TEST
        ))
        return config_handler

    @classmethod
    def setup_github_repo(cls, config_handler: ConfigHandler) -> Github:
        return Github(config_handler).with_repo(
            Repo(owner='flexiooss', repo='flexio-flow-punching-ball')
        )
