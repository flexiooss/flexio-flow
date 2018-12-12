import unittest
import os
from pathlib import Path
import shutil

from FlexioFlow.Actions.Actions import Actions
from FlexioFlow.State import State
from FlexioFlow.Version import Version
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from Schemes.Package.PackageFileHandler import PackageFileHandler
from pathlib import Path
from tests.Schemes.Package.TestPackageHelper import TestPackageHelper
from pathlib import Path
from FlexioFlow.StateHandler import StateHandler
from subprocess import PIPE, Popen
from VersionControl.GitFlow.GitFlow import GitFlow
from VersionControl.Branches import Branches
from tests.VersionControl.GitFlow.TestGitFlowHelper import TestGitFlowHelper


class TestGitFlowInit(unittest.TestCase):

    def __get_master_state(self) -> State:
        Popen(['git', 'checkout', Branches.MASTER.value], cwd=TestGitFlowHelper.DIR_PATH_TEST.as_posix()).communicate()
        state_handler_after: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST).load_file_config()
        return state_handler_after.state

    def __get_develop_state(self) -> State:
        Popen(['git', 'checkout', Branches.DEVELOP.value], cwd=TestGitFlowHelper.DIR_PATH_TEST.as_posix()).communicate()
        state_handler_after: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST).load_file_config()
        return state_handler_after.state

    def test_should_init_master_and_develop(self):
        TestGitFlowHelper.clean_workdir()
        init_version: str = '0.0.0'
        TestGitFlowHelper.mount_workdir_and_clone()
        state_handler_before: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST)
        state_handler_before.state = TestGitFlowHelper.fake_state(init_version)

        GitFlow(state_handler_before).with_branch(Branches.MASTER).set_action(Actions.INIT).process()
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
        self.assertIs(GitFlow.remote_tag_exists('0.0.0', TestGitFlowHelper.DIR_PATH_TEST), True)

        state_develop: State = self.__get_develop_state()
        self.assertEqual(
            '0.1.0',
            str(state_develop.version)
        )
        self.assertEqual(
            Level.DEV,
            state_develop.level
        )
        self.assertIs(GitFlow.remote_tag_exists('0.1.0-' + Level.DEV.value, TestGitFlowHelper.DIR_PATH_TEST), True)

        TestGitFlowHelper.clean_remote_repo()
        TestGitFlowHelper.clean_workdir()
