import json
import os
import shutil
from FlexioFlow.State import State
from FlexioFlow.Version import Version
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from Schemes.Package.PackageFileHandler import PackageFileHandler
from pathlib import Path


class TestPackageHelper:
    DIR_PATH_TEST: Path = Path('/tmp/test_package')

    PACKAGE_WITHOUT_DEV_DEPENDENCIES: str = 'package_without_dev_dependencies.json'
    PACKAGE_WITH_DEV_DEPENDENCIES: str = 'package_with_dev_dependencies.json'

    @classmethod
    def get_json_without_dev_dependencies(cls) -> dict:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/' + cls.PACKAGE_WITHOUT_DEV_DEPENDENCIES,
                  'r') as openfile:
            data = json.load(openfile)
            return data

    @classmethod
    def get_json_with_dev_dependencies(cls) -> dict:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/' + cls.PACKAGE_WITH_DEV_DEPENDENCIES,
                  'r') as openfile:
            data = json.load(openfile)
            return data

    @staticmethod
    def fake_state(version: str = '1.5.8') -> State:
        state: State = State()
        state.version = Version.from_str(version)
        state.schemes = [Schemes.PACKAGE]
        state.level = Level.STABLE
        return state

    @classmethod
    def write_package_without_dev_dependencies(cls, dir_path: Path):
        with (dir_path / PackageFileHandler.FILE_NAME).open('w') as outfile:
            json.dump(cls.get_json_without_dev_dependencies(), outfile, indent=2)

    @classmethod
    def mount_workdir_without_dev_dependencies(cls):
        cls.DIR_PATH_TEST.mkdir()
        cls.write_package_without_dev_dependencies(cls.DIR_PATH_TEST)

    @classmethod
    def write_package_with_dev_dependencies(cls, dir_path: Path):
        with (dir_path / PackageFileHandler.FILE_NAME).open('w') as outfile:
            json.dump(cls.get_json_with_dev_dependencies(), outfile, indent=2)

    @classmethod
    def mount_workdir_with_dev_dependencies(cls):
        cls.DIR_PATH_TEST.mkdir()
        cls.write_package_with_dev_dependencies(cls.DIR_PATH_TEST)

    @classmethod
    def clean_workdir(cls):
        shutil.rmtree(cls.DIR_PATH_TEST)
