import unittest

from FlexioFlow.StateHandler import StateHandler
from VersionControl.Git.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.Git.GitCmd import GitCmd

from Branches.Branches import Branches
from VersionControlProvider.Github.Repo import Repo
from tests.VersionControl.GitFlow.TestGitFlowHelper import TestGitFlowHelper

tag_test: str = 'tag_test'
git: GitCmd = GitCmd(state_handler=StateHandler(TestGitFlowHelper.DIR_PATH_TEST))

INIT_VERSION: str = '0.0.0'


class TestGitFlow(unittest.TestCase):

    def setUp(self):
        self.state_handler = TestGitFlowHelper.init_repo(INIT_VERSION)
        # self.state_handler: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST).load_file_config()
        # self.state_handler: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST)

        self.git: GitCmd = GitCmd(state_handler=self.state_handler)
        self.git_flow: GitFlowCmd = GitFlowCmd(state_handler=self.state_handler)

    def test_should_remote_tag_and_check(self):
        TestGitFlowHelper.clean_workdir()
        TestGitFlowHelper.mount_workdir_and_clone()

        self.assertIs(git.tag_exists(tag_test, remote=True), False)
        self.assertIs(git.tag_exists(tag_test, remote=False), False)

        git.checkout(Branches.MASTER).tag(tag_test).push_tag(tag_test)

        self.assertIs(git.tag_exists(tag_test, remote=True), True)
        self.assertIs(git.tag_exists(tag_test, remote=False), True)

    def tearDown(self):
        TestGitFlowHelper.clean_remote_repo()
        TestGitFlowHelper.clean_workdir()

    def test_has_hotfix(self):
        has_hotfix: bool = self.git_flow.has_hotfix(False)
        self.assertIs(has_hotfix, True)

    def test_has_conflict(self):
        self.assertIs(self.git.has_conflict(), False)
        if (self.git.has_conflict()):
            print('##################################################')
            print('conflits sur dev')
            print(self.git.get_conflict())
            print('##################################################')

    def test_get_repo(self):
        repo: Repo = self.git.get_repo()
        self.assertIsInstance(repo, Repo)
        self.assertEqual(repo.owner, 'flexiooss')
        self.assertEqual(repo.repo, 'flexio-flow-punching-ball')
