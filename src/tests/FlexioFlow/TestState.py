import unittest
from FlexioFlow.Version import Version
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.State import State
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from pathlib import Path


class TestState(unittest.TestCase):
    def setUp(self):
        self.initial_version: Version = Version(1, 8, 9)
        self.state_handler: StateHandler = StateHandler(Path('.'))
        state: State = State()
        state.version = self.initial_version
        state.level = Level.STABLE
        state.schemes = [Schemes.PACKAGE]
        self.state_handler.state = state

    def tearDown(self):
        del self.state_handler

    def test_should_bump_major(self):
        bumped_version: Version = self.state_handler.next_major()
        assert (self.state_handler.state.version is bumped_version)
        assert (self.state_handler.state.version is not self.initial_version)
        self.assertNotEqual(self.state_handler.state.version, self.initial_version)
        self.assertEqual(self.initial_version.major + 1, bumped_version.major)
        with self.assertRaises(AttributeError):
            self.state_handler.state.version.major = 12

    def test_should_bump_minor(self):
        bumped_version: Version = self.state_handler.next_minor()
        assert (self.state_handler.state.version is bumped_version)
        assert (self.state_handler.state.version is not self.initial_version)
        self.assertNotEqual(self.state_handler.state.version, self.initial_version)
        self.assertEqual(self.initial_version.minor + 1, bumped_version.minor)
        with self.assertRaises(AttributeError):
            self.state_handler.state.version.minor = 12

    def test_should_bump_patch(self):
        bumped_version: Version = self.state_handler.next_patch()
        assert (self.state_handler.state.version is bumped_version)
        assert (self.state_handler.state.version is not self.initial_version)
        self.assertNotEqual(self.state_handler.state.version, self.initial_version)
        self.assertEqual(self.initial_version.patch + 1, bumped_version.patch)
        with self.assertRaises(AttributeError):
            self.state_handler.state.version.patch = 12

    def test_should_reset_patch(self):
        reseted_version: Version = self.state_handler.reset_patch()
        assert (self.state_handler.state.version is reseted_version)
        assert (self.state_handler.state.version is not self.initial_version)
        self.assertNotEqual(self.state_handler.state.version, self.initial_version)
        self.assertEqual(0, reseted_version.patch)
        with self.assertRaises(AttributeError):
            self.state_handler.state.version.patch = 0
