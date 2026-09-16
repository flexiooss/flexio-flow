import unittest
from types import SimpleNamespace

from Branches.Actions.Issuer.IssueDefaultBuilder import IssueDefaultBuilder
from Branches.Branches import Branches
from FlexioFlow.Options import Options
from FlexioFlow.Version import Version
from VersionControlProvider.IssueDefault import IssueDefault


class TestIssueDefaultBuilder(unittest.TestCase):

    def __options(self, **kwargs) -> Options:
        options: Options = Options()
        options.branch_name = kwargs.get('branch_name', None)
        options.default = kwargs.get('default', False)
        options.major = kwargs.get('major', False)
        return options

    def __config_handler(self):
        return SimpleNamespace(config=SimpleNamespace(github=SimpleNamespace(user='nico')))

    def __state_handler(self):
        return SimpleNamespace(
            state=SimpleNamespace(version=Version(1, 2, 3)),
            get_next_patch_version=lambda: Version(1, 2, 4)
        )

    def __build(self, branch: Branches, options: Options) -> IssueDefault:
        return IssueDefaultBuilder().build(
            self.__state_handler(),
            self.__config_handler(),
            branch,
            options
        )

    def test_feature_title_comes_from_branch_name(self):
        issue: IssueDefault = self.__build(Branches.FEATURE, self.__options(branch_name='hotfix-graph', default=True))
        self.assertEqual(issue.title, 'hotfix-graph')
        self.assertEqual(issue.labels, ['enhancement'])

    def test_feature_without_branch_name_has_no_title(self):
        issue: IssueDefault = self.__build(Branches.FEATURE, self.__options())
        self.assertIsNone(issue.title)
        self.assertEqual(issue.labels, ['enhancement'])

    def test_hotfix_title_unchanged(self):
        issue: IssueDefault = self.__build(Branches.HOTFIX, self.__options(branch_name='hotfix-graph'))
        self.assertEqual(issue.title, 'Hotfix 1.2.4')
        self.assertEqual(issue.labels, ['bug', 'hotfix'])

    def test_release_title_unchanged(self):
        issue: IssueDefault = self.__build(Branches.RELEASE, self.__options(branch_name='hotfix-graph'))
        self.assertEqual(issue.title, 'Release 1.2.3')
        self.assertEqual(issue.labels, ['release'])
