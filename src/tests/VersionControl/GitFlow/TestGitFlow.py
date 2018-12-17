import unittest

from FlexioFlow.StateHandler import StateHandler
from VersionControl.GitFlow.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.GitFlow.GitCmd import GitCmd

from VersionControl.Branches import Branches
from tests.VersionControl.GitFlow.TestGitFlowHelper import TestGitFlowHelper

tag_test: str = 'tag_test'
git: GitCmd = GitCmd(state_handler=StateHandler(TestGitFlowHelper.DIR_PATH_TEST))


class TestGitFlow(unittest.TestCase):

    def setUp(self):
        # self.state_handler = TestGitFlowHelper.init_repo(INIT_VERSION)
        self.state_handler: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST).load_file_config()

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

    # def tearDown(self):
    #     git.checkout(Branches.MASTER).reset_to_tag(TestGitFlowHelper.TAG_INIT) \
    #         .push_force() \
    #         .delete_tag(tag_test, remote=True)
    #
    #     TestGitFlowHelper.clean_workdir()

    def test_has_hotfix(self):
        has_hotfix:bool = self.git_flow.has_hotfix(False)
        self.assertIs(has_hotfix, True)
