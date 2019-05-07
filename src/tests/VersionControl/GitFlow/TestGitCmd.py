import unittest
from pathlib import Path

from FlexioFlow.StateHandler import StateHandler
from VersionControl.Git.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.Git.GitCmd import GitCmd

from Branches.Branches import Branches
from VersionControlProvider.Github.Repo import Repo
from tests.VersionControl.GitFlow.TestGitFlowHelper import TestGitFlowHelper

tag_test: str = 'tag_test'
git: GitCmd = GitCmd(state_handler=StateHandler(TestGitFlowHelper.DIR_PATH_TEST))

INIT_VERSION: str = '0.0.0'


class TestGitCmd(unittest.TestCase):

    def setUp(self):
        # self.state_handler = TestGitFlowHelper.init_repo(INIT_VERSION)
        # # self.state_handler: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST).load_file_config()
        self.state_handler: StateHandler = StateHandler(Path('/tmp/test'))

        self.git: GitCmd = GitCmd(state_handler=self.state_handler)
        self.git_flow: GitFlowCmd = GitFlowCmd(state_handler=self.state_handler)

    def test_has_branch(self):
        has_branch: bool = self.git.local_branch_exists('hotfix')
        self.assertTrue(has_branch)

    def test_current_branch(self):
        branch_name: str = self.git.get_current_branch_name()
        print(branch_name)

    def test_has_tag(self):
        has_tag: bool = self.git.tag_exists('0.0.0')
        self.assertTrue(has_tag)

    def test_has_not_tag(self):
        has_tag: bool = self.git.tag_exists('0.1.0')
        self.assertFalse(has_tag)

    def test_has_remote(self):
        has_remote: bool = self.git.has_remote()
        print(has_remote)
