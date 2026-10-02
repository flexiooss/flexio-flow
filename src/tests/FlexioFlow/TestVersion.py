import unittest

from FlexioFlow.Level import Level
from FlexioFlow.Version import Version


class TestVersion(unittest.TestCase):

    def setUp(self):
        self.version: Version = Version(1, 8, 9)

    def tearDown(self):
        del self.version

    # def test_enum(self):
    #     try:
    #         ma_var = Level['tutu']
    #         print(ma_var)
    #     except KeyError:
    #         print('tampis')

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

    def test_should_parse_four_components(self):
        version: Version = Version.from_str('1.29.0.1')
        self.assertEqual(1, version.major)
        self.assertEqual(29, version.minor)
        self.assertEqual(0, version.patch)
        self.assertEqual(1, version.support)

    def test_should_parse_three_components_with_no_support(self):
        version: Version = Version.from_str('1.29.0')
        self.assertIsNone(version.support)

    def test_should_print_three_components_when_no_support(self):
        self.assertEqual('1.29.0', str(Version(1, 29, 0)))

    def test_should_print_four_components_with_support(self):
        self.assertEqual('1.29.0.1', str(Version(1, 29, 0, 1)))

    def test_should_omit_support_key_when_none(self):
        self.assertEqual({'major': 1, 'minor': 29, 'patch': 0}, Version(1, 29, 0).to_dict())

    def test_should_bump_support_from_three_components(self):
        self.assertEqual('1.29.0.1', str(Version(1, 29, 0).next_support()))

    def test_should_bump_support_from_four_components(self):
        self.assertEqual('1.29.0.2', str(Version(1, 29, 0, 1).next_support()))

    def test_should_erase_support_on_next_minor(self):
        self.assertEqual('1.30.0', str(Version(1, 29, 0, 1).next_minor()))

    def test_should_erase_support_on_next_patch(self):
        self.assertEqual('1.29.1', str(Version(1, 29, 0, 1).next_patch()))

    def test_should_erase_support_on_next_major(self):
        self.assertEqual('2.0.0', str(Version(1, 29, 0, 1).next_major()))

    def test_should_refuse_five_components(self):
        with self.assertRaises(ValueError):
            Version.from_str('1.29.0.1.2')
