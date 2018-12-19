import unittest
from pathlib import Path

from requests import Response

from Core.Config import Config
from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Github.ConfigGithub import ConfigGithub
from VersionControlProvider.Github.Github import Github

TOKEN_TEST: str = 'daca8bdd8c905bbae9637b6d2e98b1a3ea238747'
USER: str = 'thomas@flexio.fr'
CONFIG_DIR: Path = Path('/tmp/')


class TestGithub(unittest.TestCase):

    def setUp(self):
        self.config_handler = ConfigHandler(CONFIG_DIR)
        self.config_handler.config = Config(ConfigGithub(
            activate=True,
            user=USER,
            token=TOKEN_TEST
        ))

    #     # self.state_handler = TestGitFlowHelper.init_repo(INIT_VERSION)
    #     # self.state_handler: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST).load_file_config()
    #     self.state_handler: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST)
    #
    #     self.git: GitCmd = GitCmd(state_handler=self.state_handler)
    #     self.git_flow: GitFlowCmd = GitFlowCmd(state_handler=self.state_handler)

    def test_get_user(self):
        r: Response = Github(self.config_handler).get_user()
        self.assertIs(r.status_code, 200)

        falsy_config_handler = ConfigHandler(CONFIG_DIR)
        falsy_config_handler.config = Config(ConfigGithub(
            activate=True,
            user=USER,
            token=TOKEN_TEST
        ))
        r: Response = Github(falsy_config_handler).get_user()
        self.assertIs(r.status_code, 200)
