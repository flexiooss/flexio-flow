import json
import os
import shutil
from FlexioFlow.State import State
from FlexioFlow.Version import Version
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from Schemes.Package.PackageFileHandler import PackageFileHandler
from pathlib import Path
from tests.Schemes.Package.TestPackageHelper import TestPackageHelper
from pathlib import Path
from FlexioFlow.StateHandler import StateHandler


class TestSchemesHelper:
    DIR_PATH_TEST: Path = Path('/tmp/test_flexioflow')

    @staticmethod
    def fake_state(version: str = '1.5.8') -> State:
        state: State = State()
        state.version = Version.from_str(version)
        state.schemes = [Schemes.PACKAGE]
        state.level = Level.STABLE
        return state

    @classmethod
    def fake_state_handler(cls) -> StateHandler:
        state_handler: StateHandler = StateHandler(cls.DIR_PATH_TEST)
        state_handler.state = cls.fake_state()
        return state_handler

    @classmethod
    def mount_workdir_without_dev_dependencies(cls):
        cls.DIR_PATH_TEST.mkdir()
        cls.fake_state_handler().write_file()
        with (TestSchemesHelper.DIR_PATH_TEST / PackageFileHandler.FILE_NAME).open('w') as outfile:
            json.dump(TestPackageHelper.get_json_without_dev_dependencies(), outfile, indent=2)


    @classmethod
    def mount_workdir_with_dev_dependencies(cls):
        cls.DIR_PATH_TEST.mkdir()
        cls.fake_state_handler().write_file()
        with (TestSchemesHelper.DIR_PATH_TEST / PackageFileHandler.FILE_NAME).open('w') as outfile:
            json.dump(TestPackageHelper.get_json_with_dev_dependencies(), outfile, indent=2)

    @classmethod
    def clean_workdir(cls):
        shutil.rmtree(cls.DIR_PATH_TEST)
