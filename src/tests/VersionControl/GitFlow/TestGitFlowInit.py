import unittest
from FlexioFlow.State import State
from FlexioFlow.Level import Level
from FlexioFlow.StateHandler import StateHandler
from VersionControl.Git.GitCmd import GitCmd
from Branches.Branches import Branches
from tests.VersionControl.GitFlow.TestGitFlowHelper import TestGitFlowHelper

INIT_VERSION: str = '0.0.0'
git: GitCmd = GitCmd(state_handler=StateHandler(TestGitFlowHelper.DIR_PATH_TEST))


class TestGitFlowInit(unittest.TestCase):

    def tearDown(self):
        TestGitFlowHelper.clean_remote_repo()
        TestGitFlowHelper.clean_workdir()

    def __get_master_state(self) -> State:
        git.checkout(Branches.MASTER)

        state_handler_after: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST).load_file_config()
        return state_handler_after.state

    def __get_develop_state(self) -> State:
        git.checkout(Branches.DEVELOP)

        state_handler_after: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST).load_file_config()
        return state_handler_after.state

    def test_should_init_master_and_develop(self):
        # TestGitFlowHelper.clean_remote_repo()

        state_handler_before: StateHandler = TestGitFlowHelper.init_repo(INIT_VERSION)
        TestGitFlowHelper.clean_workdir()

        TestGitFlowHelper.mount_workdir_and_clone()
        state_master: State = self.__get_master_state()
        self.assertEqual(
            '0.0.0',
            str(state_master.version)
        )
        self.assertEqual(
            Level.STABLE,
            state_master.level
        )
        self.assertIs(git.tag_exists('0.0.0', remote=True), True)

        state_develop: State = self.__get_develop_state()
        self.assertEqual(
            '0.1.0',
            str(state_develop.version)
        )
        self.assertEqual(
            Level.DEV,
            state_develop.level
        )
