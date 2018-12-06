import unittest
from Exceptions.FileNotExistError import FileNotExistError
from Schemes.Package.PackageScheme import PackageScheme
from Schemes.Package.PackageFileHandler import PackageFileHandler
import os
import json
import shutil
from tests.Schemes.Package.TestPackageHelper import TestPackageHelper
from FlexioFlow.State import State
from FlexioFlow.Version import Version
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes


class TestPackageScheme(unittest.TestCase):
    DIR_PATH_TEST = '/tmp/test_package'

    def setUp(self):
        os.mkdir(self.DIR_PATH_TEST)
        with open(self.DIR_PATH_TEST + '/' + PackageFileHandler.FILE_NAME, 'w') as outfile:
            json.dump(TestPackageHelper.get_json_without_dev_dependencies(), outfile, indent=2)
        outfile.close()

    def tearDown(self):
        shutil.rmtree(self.DIR_PATH_TEST)

    def test_should_find_file_or_raise(self):
        PackageFileHandler(self.DIR_PATH_TEST + '/')
        with self.assertRaises(FileNotExistError):
            PackageFileHandler('nothing')

    def test_should_change_version(self):
        new_version: str = '1.5.8'

        state: State = State()
        state.version = Version.from_str(new_version)
        state.scheme = [Schemes.PACKAGE]
        state.level = Level.STABLE

        package_handler_before = PackageFileHandler(self.DIR_PATH_TEST + '/')
        self.assertNotEqual(
            new_version,
            package_handler_before.get_version()
        )
        package: PackageScheme = PackageScheme(self.DIR_PATH_TEST + '/', state)
        package.set_version()

        package_handler_after = PackageFileHandler(self.DIR_PATH_TEST + '/')
        self.assertEqual(
            new_version,
            package_handler_after.get_version()
        )


if __name__ == '__main__':
    unittest.main()
