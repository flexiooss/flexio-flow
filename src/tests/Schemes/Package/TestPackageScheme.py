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
from Schemes.Dependencies import Dependencies


class TestPackageScheme(unittest.TestCase):

    def tearDown(self):
        TestPackageHelper.clean_workdir()

    def test_should_find_file_or_raise(self):
        TestPackageHelper.mount_workdir_without_dev_dependencies()

        PackageFileHandler(TestPackageHelper.DIR_PATH_TEST + '/')
        with self.assertRaises(FileNotExistError):
            PackageFileHandler('nothing')

    def test_should_change_version(self):
        TestPackageHelper.mount_workdir_without_dev_dependencies()
        state: State = TestPackageHelper.fake_state()

        package_handler_before = PackageFileHandler(TestPackageHelper.DIR_PATH_TEST + '/')
        self.assertNotEqual(
            str(state.version),
            package_handler_before.get_version()
        )
        package: PackageScheme = PackageScheme(TestPackageHelper.DIR_PATH_TEST + '/', state)
        package.set_version()

        package_handler_after = PackageFileHandler(TestPackageHelper.DIR_PATH_TEST + '/')
        self.assertEqual(
            str(state.version),
            package_handler_after.get_version()
        )

    def test_should_plan_release_empty(self):
        TestPackageHelper.mount_workdir_without_dev_dependencies()
        state: State = TestPackageHelper.fake_state()
        package: PackageScheme = PackageScheme(TestPackageHelper.DIR_PATH_TEST + '/', state)
        dependencies: Dependencies = package.release_precheck()

        self.assertIsInstance(dependencies, Dependencies)
        self.assertEqual(len(dependencies), 0)

    def test_should_plan_release_not_empty(self):
        TestPackageHelper.mount_workdir_with_dev_dependencies()
        state: State = TestPackageHelper.fake_state()
        package: PackageScheme = PackageScheme(TestPackageHelper.DIR_PATH_TEST + '/', state)
        dependencies: Dependencies = package.release_precheck()

        self.assertIsInstance(dependencies, Dependencies)
        self.assertNotEqual(len(dependencies), 0)


if __name__ == '__main__':
    unittest.main()
