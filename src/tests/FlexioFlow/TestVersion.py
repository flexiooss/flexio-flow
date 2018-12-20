import unittest

from FlexioFlow.Level import Level
from FlexioFlow.Version import Version


class TestVersion(unittest.TestCase):

    def setUp(self):
        self.version: Version = Version(1, 8, 9)

    def tearDown(self):
        del self.version

    def test_enum(self):
        Level
        try:
            ma_var = Level['tutu']
            print(ma_var)
        except KeyError:
            print('tampis')

    def test_should_bump_major(self):
        bumped_version: Version = self.version.next_major()
        assert (self.version is not bumped_version)
        self.assertNotEqual(self.version, bumped_version)
        self.assertEqual(self.version.major + 1, bumped_version.major)
        with self.assertRaises(AttributeError):
            self.version.major = 12

    def test_should_bump_minor(self):
        bumped_version: Version = self.version.next_minor()
        assert (self.version is not bumped_version)
        self.assertNotEqual(self.version, bumped_version)
        self.assertEqual(self.version.minor + 1, bumped_version.minor)
        with self.assertRaises(AttributeError):
            self.version.minor = 12

    def test_should_bump_patch(self):
        bumped_version: Version = self.version.next_patch()
        assert (self.version is not bumped_version)
        self.assertNotEqual(self.version, bumped_version)
        self.assertEqual(self.version.patch + 1, bumped_version.patch)
        with self.assertRaises(AttributeError):
            self.version.patch = 12

    def test_should_reset_patch(self):
        reseted_version: Version = self.version.reset_patch()
        assert (self.version is not reseted_version)
        self.assertNotEqual(self.version, reseted_version)
        self.assertEqual(0, reseted_version.patch)
        with self.assertRaises(AttributeError):
            self.version.patch = 0
