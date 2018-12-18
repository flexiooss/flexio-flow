import unittest
from pathlib import Path
from VersionControlProvider.Github.Github import Github

TOKEN_TEST: str = 'caca12daca8bdd8c905bbae9637b6d2e98b1a3ea23874712prout'
USER: str = 'thomas@flexio.io'
CONFIG_DIR: Path = Path('/tmp')


class TestGithub(unittest.TestCase):

    # def setUp(self):
    #     # self.state_handler = TestGitFlowHelper.init_repo(INIT_VERSION)
    #     # self.state_handler: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST).load_file_config()
    #     self.state_handler: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST)
    #
    #     self.git: GitCmd = GitCmd(state_handler=self.state_handler)
    #     self.git_flow: GitFlowCmd = GitFlowCmd(state_handler=self.state_handler)

    def test_get_user(self):
        Github(CONFIG_DIR).with_token(TOKEN_TEST).get_user()
