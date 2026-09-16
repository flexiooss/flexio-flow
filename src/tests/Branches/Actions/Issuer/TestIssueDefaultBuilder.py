import unittest
from unittest.mock import MagicMock

from Branches.Actions.Issuer.IssueDefaultBuilder import IssueDefaultBuilder
from Branches.Branches import Branches
from FlexioFlow.Options import Options
from FlexioFlow.Version import Version
from VersionControlProvider.IssueDefault import IssueDefault


class TestIssueDefaultBuilder(unittest.TestCase):

    def setUp(self):
        self.state_handler = MagicMock()
        self.state_handler.state.version = Version.from_str('1.29.0')
        self.state_handler.get_next_patch_version.return_value = Version.from_str('1.29.1')
        self.config_handler = MagicMock()
        self.config_handler.config.github.user = 'a-user'
        self.options = Options()

    def build(self, branch) -> IssueDefault:
        return IssueDefaultBuilder().build(self.state_handler, self.config_handler, branch, self.options)

    def test_release_has_a_default_title(self):
        issue = self.build(Branches.RELEASE)
        self.assertEqual(issue.title, 'Release 1.29.0')
        self.assertEqual(issue.labels, ['release'])

    def test_hotfix_has_a_default_title_naming_the_next_patch(self):
        issue = self.build(Branches.HOTFIX)
        self.assertEqual(issue.title, 'Hotfix 1.29.1')
        self.assertEqual(issue.labels, ['bug', 'hotfix'])

    def test_hotfix_title_is_set_so_default_option_does_not_prompt(self):
        self.assertIsNotNone(self.build(Branches.HOTFIX).title)
