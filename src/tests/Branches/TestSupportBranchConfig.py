import unittest

from Branches.BranchHandler import BranchHandler
from Branches.Branches import Branches
from Branches.BranchesConfig import BranchesConfig
from FlexioFlow.Version import Version


class TestSupportBranchConfig(unittest.TestCase):

    def setUp(self):
        self.branches: BranchesConfig = BranchesConfig.from_dict({})

    def test_cli_token_is_support_branch(self):
        self.assertEqual('support-branch', Branches.SUPPORT_BRANCH.value)
        self.assertTrue(Branches.has_value('support-branch'))

    def test_executor_lookup_maps_hyphen_to_underscore(self):
        self.assertIs(Branches.SUPPORT_BRANCH, Branches['support-branch'.upper().replace('-', '_')])

    def test_git_prefix_is_support(self):
        self.assertEqual('support', self.branches.support)

    def test_is_support_compares_by_value(self):
        self.assertTrue(self.branches.is_support('support'))
        self.assertFalse(self.branches.is_support('hotfix'))

    def test_to_dict_carries_support(self):
        self.assertEqual('support', self.branches.to_dict().get('support'))

    def test_branch_name_from_support_version(self):
        name: str = BranchHandler('support', self.branches).branch_name_from_version(Version(1, 29, 0, 1))
        self.assertEqual('support/1.29.0.1-dev', name)
