import json
import os
import shutil
from FlexioFlow.State import State
from FlexioFlow.Version import Version
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from Schemes.Package.PackageFileHandler import PackageFileHandler


class TestPackageHelper:
    DIR_PATH_TEST = '/tmp/test_package'

    PACKAGE_WITHOUT_DEV_DEPENDENCIES = 'package_without_dev_dependencies.json'
    PACKAGE_WITH_DEV_DEPENDENCIES = 'package_with_dev_dependencies.json'

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
    def fake_state() -> State:
        state: State = State()
        state.version = Version.from_str('1.5.8')
        state.scheme = [Schemes.PACKAGE]
        state.level = Level.STABLE
        return state

    @classmethod
    def mount_workdir_without_dev_dependencies(cls):
        os.mkdir(cls.DIR_PATH_TEST)
        with open(cls.DIR_PATH_TEST + '/' + PackageFileHandler.FILE_NAME, 'w') as outfile:
            json.dump(cls.get_json_without_dev_dependencies(), outfile, indent=2)

    @classmethod
    def mount_workdir_with_dev_dependencies(cls):
        os.mkdir(cls.DIR_PATH_TEST)
        with open(cls.DIR_PATH_TEST + '/' + PackageFileHandler.FILE_NAME, 'w') as outfile:
            json.dump(cls.get_json_with_dev_dependencies(), outfile, indent=2)

    @classmethod
    def clean_workdir(cls):
        shutil.rmtree(cls.DIR_PATH_TEST)