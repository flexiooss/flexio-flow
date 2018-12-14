import unittest

from FlexioFlow.StateHandler import StateHandler
from VersionControl.GitFlow.GitCmd import GitCmd

from VersionControl.Branches import Branches
from tests.VersionControl.GitFlow.TestGitFlowHelper import TestGitFlowHelper

tag_test: str = 'tag_test'
git: GitCmd = GitCmd(state_handler=StateHandler(TestGitFlowHelper.DIR_PATH_TEST))


class TestGitFlow(unittest.TestCase):
    def test_should_remote_tag_and_check(self):
        TestGitFlowHelper.clean_workdir()
        TestGitFlowHelper.mount_workdir_and_clone()

        self.assertIs(git.tag_exists(tag_test, remote=True), False)
        self.assertIs(git.tag_exists(tag_test, remote=False), False)

        git.checkout(Branches.MASTER).tag(tag_test).push_tag(tag_test)

        self.assertIs(git.tag_exists(tag_test, remote=True), True)
        self.assertIs(git.tag_exists(tag_test, remote=False), True)

    def tearDown(self):
        git.checkout(Branches.MASTER).reset_to_tag(TestGitFlowHelper.TAG_INIT) \
            .push_force() \
            .delete_tag(tag_test, remote=True)

        TestGitFlowHelper.clean_workdir()
