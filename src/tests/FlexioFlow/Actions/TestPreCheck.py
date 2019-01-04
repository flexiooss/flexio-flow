import unittest
from tests.Schemes.TestSchemesHelper import TestSchemesHelper
from FlexioFlow.StateHandler import StateHandler
from VersionControl.VersionController import VersionController
from Branches.Actions.Actions import Actions
from Branches.Branches import Branches
from typing import Type
from VersionControl.VersionControl import VersionControl
from VersionControl.VersionControlFactory import VersionControlFactory
from Branches.Actions.ActionFactory import ActionFactory
from Branches.Actions.Action import Action
from Exceptions.HaveDevDependencyException import HaveDevDependencyException


class TestPreCheck(unittest.TestCase):
    def tearDown(self):
        TestSchemesHelper.clean_workdir()

    def test_should_dev_dependencies_empty(self):
        TestSchemesHelper.mount_workdir_without_dev_dependencies()
        state_handler: StateHandler = StateHandler(TestSchemesHelper.DIR_PATH_TEST).load_file_config()

        version_control: Type[VersionControl] = VersionControlFactory.build(
            VersionController.GITFLOW,
            state_handler
        )
        action: Type[Action] = ActionFactory.build(
            Actions.PRECHECK,
            version_control,
            Branches.RELEASE,
            state_handler,
            {}
        ).process()

    def test_should_dev_dependencies_not_empty(self):
        TestSchemesHelper.mount_workdir_with_dev_dependencies()
        state_handler: StateHandler = StateHandler(TestSchemesHelper.DIR_PATH_TEST).load_file_config()

        version_control: Type[VersionControl] = VersionControlFactory.build(
            VersionController.GITFLOW,
            state_handler
        )
        action: Type[Action] = ActionFactory.build(
            Actions.PRECHECK,
            version_control,
            Branches.RELEASE,
            state_handler,
            {}
        )
        with self.assertRaises(HaveDevDependencyException):
            action.process()
