import unittest

from FlexioFlow.Actions.Actions import Actions
from FlexioFlow.State import State
from FlexioFlow.Level import Level
from FlexioFlow.StateHandler import StateHandler
from VersionControl.GitFlow.GitCmd import GitCmd
from VersionControl.Branches import Branches
from VersionControl.GitFlow.GitFlow import GitFlow
from tests.VersionControl.GitFlow.TestGitFlowHelper import TestGitFlowHelper

git: GitCmd = GitCmd(state_handler=StateHandler(TestGitFlowHelper.DIR_PATH_TEST))
INIT_VERSION: str = '0.0.0'


class TestGitFlowHotfix(unittest.TestCase):
    state_handler: StateHandler

    def __hotfix_start(self):
        GitFlow(self.state_handler).with_branch(Branches.HOTFIX).set_action(Actions.START).process()

    def __hotfix_finish(self):
        GitFlow(self.state_handler).with_branch(Branches.HOTFIX).set_action(Actions.FINISH).process()

    def __get_master_state(self) -> State:
        git.checkout(Branches.MASTER)

        state_handler_after: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST).load_file_config()
        return state_handler_after.state

    def __get_hotfix_state(self) -> State:
        git.checkout(Branches.HOTFIX)
        state_handler_after: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST).load_file_config()
        return state_handler_after.state

    # def tearDown(self):
    #     git.delete_branch('hotfix/0.0.1-dev')
    #     TestGitFlowHelper.clean_remote_repo()
    #     TestGitFlowHelper.clean_workdir

    def setUp(self):
        TestGitFlowHelper.clean_workdir()
        TestGitFlowHelper.init_repo(INIT_VERSION)
        git.delete_branch('hotfix/0.0.1-dev', remote=True)
        TestGitFlowHelper.clean_remote_repo()
        TestGitFlowHelper.clean_workdir()

    def test_vide(self):
        pass

    # def test_should_start_hotfix(self):
    #     self.state_handler = TestGitFlowHelper.init_repo(INIT_VERSION)
    #     self.__hotfix_start()
    #
    #     self.assertIs(git.branch_exists('hotfix/0.0.1-dev', remote=True), True)
    #
    #     state_master: State = self.__get_master_state()
    #     self.assertEqual(
    #         '0.0.0',
    #         str(state_master.version)
    #     )
    #     self.assertEqual(
    #         Level.STABLE,
    #         state_master.level
    #     )
    #
    #     state_hotfix: State = self.__get_hotfix_state()
    #     self.assertEqual(
    #         '0.0.1',
    #         str(state_hotfix.version)
    #     )
    #     self.assertEqual(
    #         Level.DEV,
    #         state_hotfix.level
    #     )


    # def test_should_finish_hotfix(self):
    #     self.state_handler = TestGitFlowHelper.init_repo(INIT_VERSION)
    #     self.__hotfix_start()
    #     self.__hotfix_finish()
    #
    #     state_master: State = self.__get_master_state()
    #     self.assertEqual(
    #         '0.0.1',
    #         str(state_master.version)
    #     )
    #     self.assertEqual(
    #         Level.STABLE,
    #         state_master.level
    #     )
    #     self.assertIs(git.branch_exists('hotfix/0.0.1-dev', remote=True), False)
    #
    #     self.assertIs(git.tag_exists('0.0.1', remote=True), True)

        # git.delete_tag('0.0.1', remote=True)
