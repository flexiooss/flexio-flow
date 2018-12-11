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
    def test_should_init_master_and_develop(self):
        init_version: str = '0.0.0'
        TestGitFlowHelper.mount_workdir_and_clone()
        state_handler: StateHandler = StateHandler(TestGitFlowHelper.DIR_PATH_TEST)
        state_handler.state = TestGitFlowHelper.fake_state(init_version)

        GitFlow(state_handler).with_branch(Branches.MASTER).set_action(Actions.INIT).process()
