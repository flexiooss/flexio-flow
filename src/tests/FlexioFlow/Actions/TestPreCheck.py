import unittest
from tests.Schemes.TestSchemesHelper import TestSchemesHelper
from FlexioFlow.StateHandler import StateHandler
from VersionControl.VersionController import VersionController
from FlexioFlow.Actions.Actions import Actions
from VersionControl.Branches import Branches
from typing import Type
from VersionControl.VersionControl import VersionControl
from VersionControl.VersionControlFactory import VersionControlFactory
from FlexioFlow.Actions.ActionFactory import ActionFactory
from FlexioFlow.Actions.Action import Action
from Exceptions.HaveDevDependencyException import HaveDevDependencyException


class TestPreCheck(unittest.TestCase):
    def tearDown(self):
        TestSchemesHelper.clean_workdir()

    def test_should_dev_dependencies_empty(self):
        TestSchemesHelper.mount_workdir_without_dev_dependencies()
        state_handler: StateHandler = StateHandler(TestSchemesHelper.DIR_PATH_TEST).load_file_config()

        version_control: Type[VersionControl] = VersionControlFactory.create(
            VersionController.GITFLOW,
            state_handler
        )
        action: Type[Action] = ActionFactory.create(
            Actions.PRECHECK,
            version_control,
            Branches.RELEASE,
            state_handler,
            {}
        ).process()

    def test_should_dev_dependencies_not_empty(self):
        TestSchemesHelper.mount_workdir_with_dev_dependencies()
        state_handler: StateHandler = StateHandler(TestSchemesHelper.DIR_PATH_TEST).load_file_config()

        version_control: Type[VersionControl] = VersionControlFactory.create(
            VersionController.GITFLOW,
            state_handler
        )
        action: Type[Action] = ActionFactory.create(
            Actions.PRECHECK,
            version_control,
            Branches.RELEASE,
            state_handler,
            {}
        )
        with self.assertRaises(HaveDevDependencyException):
            action.process()
