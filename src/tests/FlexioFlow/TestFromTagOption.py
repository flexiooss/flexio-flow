import unittest
from pathlib import Path

from Branches.Actions.Issuer.IssueDefaultBuilder import IssueDefaultBuilder
from Branches.Branches import Branches
from Branches.BranchesConfig import BranchesConfig
from Core.Config import Config
from Core.ConfigHandler import ConfigHandler
from FlexioFlow.Options import Options
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.options.FromTag import FromTag
from FlexioFlow.options.Resolver import Resolver
from VersionControlProvider.Github.ConfigGithub import ConfigGithub
from VersionControlProvider.IssueDefault import IssueDefault


class TestFromTagOption(unittest.TestCase):

    def test_should_read_from_tag_value(self):
        options: Options = Options()
        FromTag.process(opt='--from-tag', arg='1.29.0', options=options)
        self.assertEqual('1.29.0', options.from_tag)

    def test_should_default_to_none(self):
        self.assertIsNone(Options().from_tag)

    def test_should_not_collide_with_from(self):
        options: Options = Options()
        FromTag.process(opt='--from', arg='maven', options=options)
        self.assertIsNone(options.from_tag)

    def test_resolver_declares_the_long_option(self):
        self.assertIn('from-tag=', Resolver().name_options())

    def __issue_for(self, options: Options) -> IssueDefault:
        config_handler: ConfigHandler = ConfigHandler(Path('/tmp/test_flexioflow_issue_config'))
        config_handler.config = Config().with_github(
            ConfigGithub(activate=False, user='u', token='t')
        ).with_branches_config(BranchesConfig.from_dict({}))
        return IssueDefaultBuilder().build(
            state_handler=StateHandler(Path('/tmp')),
            config_handler=config_handler,
            branch=Branches.SUPPORT_BRANCH,
            options=options
        )

    def test_issue_title_carries_the_tag(self):
        options: Options = Options()
        options.from_tag = '1.29.0'
        issue: IssueDefault = self.__issue_for(options)
        self.assertEqual('Support 1.29.0', issue.title)
        self.assertIn('support', issue.labels)

    def test_issue_title_without_tag(self):
        self.assertEqual('Support', self.__issue_for(Options()).title)
