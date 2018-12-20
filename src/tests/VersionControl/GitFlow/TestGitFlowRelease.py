import unittest

from Exceptions.BranchNotExist import BranchNotExist
from FlexioFlow.Actions.Actions import Actions
from FlexioFlow.State import State
from FlexioFlow.Level import Level
from FlexioFlow.StateHandler import StateHandler
from VersionControl.GitFlow.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.GitFlow.GitCmd import GitCmd
from Branches.Branches import Branches
from VersionControl.GitFlow.GitFlow import GitFlow
from tests.VersionControl.GitFlow.TestGitFlowHelper import TestGitFlowHelper

INIT_VERSION: str = '0.0.0'


class TestGitFlowRelease(unittest.TestCase):
    state_handler: StateHandler

    def __release_start(self):
        GitFlow(self.state_handler).build_branch(Branches.RELEASE).set_action(Actions.START).process()

    def __release_finish(self):
        GitFlow(self.state_handler).build_branch(Branches.RELEASE).set_action(Actions.FINISH).process()

    def __get_master_state(self) -> State:
        self.git.checkout(Branches.MASTER)
        return self.state_handler.state

    def __get_release_state(self) -> State:
        print('__get_release_state')
        self.git.checkout(Branches.RELEASE)
        return self.state_handler.state

    def __get_dev_state(self) -> State:
        self.git.checkout(Branches.DEVELOP)
        return self.state_handler.state

    # def tearDown(self):
    #     git.delete_branch_from_name('hotfix/0.0.1-dev')
    #     TestGitFlowHelper.clean_remote_repo()
    #     TestGitFlowHelper.clean_workdir

    def setUp(self):
        TestGitFlowHelper.clean_workdir()
        TestGitFlowHelper.init_repo(INIT_VERSION)
        GitCmd(state_handler=StateHandler(TestGitFlowHelper.DIR_PATH_TEST)).delete_branch_from_name(
            'release/0.1.0',
            remote=True
        ).delete_tag('0.1.0', remote=True)

        TestGitFlowHelper.clean_remote_repo()
        TestGitFlowHelper.clean_workdir()

        # def setUp(self):
        self.state_handler = TestGitFlowHelper.init_repo(INIT_VERSION)
        # state_handler_after: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST).load_file_config()

        self.git: GitCmd = GitCmd(state_handler=self.state_handler)
        self.git_flow: GitFlowCmd = GitFlowCmd(state_handler=self.state_handler)

    # def test_vide(self):
    #     pass

    # def test_should_start_release(self):
    #     self.assertIs(self.git.branch_exists_from_name('release/0.1.0', remote=True), False)
    #     self.assertIs(self.git.branch_exists_from_name('release/0.1.0', remote=False), False)
    #
    #     self.__release_start()
    #
    #     self.assertIs(self.git.branch_exists_from_name('release/0.1.0', remote=False), True)
    #     self.assertIs(self.git.branch_exists_from_name('release/0.1.0', remote=True), True)
    #
    #     state_master: State = self.__get_master_state()
    #     self.assertEqual(
    #         '0.0.0',
    #         INIT_VERSION
    #     )
    #     self.assertEqual(
    #         Level.STABLE,
    #         state_master.level
    #     )
    #
    #     state_dev: State = self.__get_dev_state()
    #     self.assertEqual(
    #         '0.1.0',
    #         str(state_dev.version)
    #     )
    #     self.assertEqual(
    #         Level.DEV,
    #         state_dev.level
    #     )
    #
    #     state_release: State = self.__get_release_state()
    #     self.assertEqual(
    #         '0.1.0',
    #         str(state_release.version)
    #     )
    #     self.assertEqual(
    #         Level.STABLE,
    #         state_release.level
    #     )
    #     with self.assertRaises(BranchAlreadyExist):
    #         self.__release_start()

    def test_should_finish_release(self):
        with self.assertRaises(BranchNotExist):
            self.__release_finish()

        self.__release_start()
        self.__release_finish()

        state_master: State = self.__get_master_state()
        self.assertEqual(
            '0.1.0',
            str(state_master.version)
        )
        self.assertEqual(
            Level.STABLE,
            state_master.level
        )
        self.assertIs(self.git.branch_exists_from_name('release/0.1.0', remote=True), False)

        self.assertIs(self.git.tag_exists('0.1.0', remote=False), True, 'Tag local should be 0.1.0')
        self.assertIs(self.git.tag_exists('0.1.0', remote=True), True, 'Tag remote should be 0.1.0')

        state_dev: State = self.__get_dev_state()
        self.assertEqual(
            '0.2.0',
            str(state_dev.version)
        )
        self.assertEqual(
            Level.DEV,
            state_dev.level
        )
