import unittest
from pathlib import Path

from Branches.BranchesConfig import BranchesConfig
from Core.Config import Config
from Core.ConfigHandler import ConfigHandler
from Exceptions.AmbiguousTagAtHead import AmbiguousTagAtHead
from Exceptions.NoTagAtHead import NoTagAtHead
from Exceptions.TagIsMasterTip import TagIsMasterTip
from Exceptions.TagNotFound import TagNotFound
from Exceptions.TagNotPushed import TagNotPushed
from Exceptions.TagVersionMismatch import TagVersionMismatch
from FlexioFlow.Options import Options
from FlexioFlow.StateHandler import StateHandler
from VersionControl.Git.Branches.SupportBranch.Start import Start
from VersionControl.Git.GitCmd import GitCmd
from tests.VersionControl.GitFlow.LocalRepo import LocalRepo


class TestGitFlowSupportBranch(unittest.TestCase):
    PATH: Path = Path('/tmp/test_flexioflow_support')

    def setUp(self):
        LocalRepo.create(self.PATH)
        self.__advance_master()
        self.state_handler: StateHandler = StateHandler(self.PATH)
        self.state_handler.load_file_config()
        self.config_handler: ConfigHandler = ConfigHandler(Path('/tmp/test_flexioflow_support_config'))
        self.config_handler.config = Config().with_branches_config(BranchesConfig.from_dict({}))
        self.git: GitCmd = GitCmd(state_handler=self.state_handler)

    def tearDown(self):
        LocalRepo.clean(self.PATH)
        LocalRepo.clean(Path(self.PATH.as_posix() + '_remote.git'))

    def __advance_master(self) -> None:
        (self.PATH / 'master.txt').write_text('master moved on\n')
        LocalRepo.run(self.PATH, ['git', 'add', '.'])
        LocalRepo.run(self.PATH, ['git', 'commit', '-qm', 'master moved on'])
        LocalRepo.run(self.PATH, ['git', 'checkout', '-q', 'develop'])
        LocalRepo.run(self.PATH, ['git', 'merge', '-q', 'master'])
        LocalRepo.run(self.PATH, ['git', 'checkout', '-q', 'master'])

    def __start(self, from_tag=None) -> None:
        options: Options = Options()
        options.from_tag = from_tag
        Start(
            state_handler=self.state_handler,
            config_handler=self.config_handler,
            issue=None,
            topics=None,
            options=options
        ).process()

    def test_should_create_branch_from_tag_with_support_version(self):
        self.__start(from_tag='1.29.0')
        self.assertEqual('support/1.29.0.1-dev', LocalRepo.run(self.PATH, ['git', 'branch', '--show-current']))
        self.state_handler.load_file_config()
        self.assertEqual('1.29.0.1', self.state_handler.version_as_str())

    def test_should_resolve_tag_from_head_when_option_absent(self):
        LocalRepo.run(self.PATH, ['git', 'checkout', '-q', '1.29.0'])
        self.__start()
        self.assertEqual('support/1.29.0.1-dev', LocalRepo.run(self.PATH, ['git', 'branch', '--show-current']))

    def test_should_refuse_when_head_is_not_on_a_version_tag(self):
        with self.assertRaises(NoTagAtHead):
            self.__start()

    def test_should_refuse_when_several_version_tags_at_head(self):
        LocalRepo.run(self.PATH, ['git', 'tag', '-a', '1.30.0', '-m', 'dup', '1.29.0'])
        LocalRepo.run(self.PATH, ['git', 'checkout', '-q', '1.29.0'])
        with self.assertRaises(AmbiguousTagAtHead):
            self.__start()

    def test_should_refuse_unknown_tag(self):
        with self.assertRaises(TagNotFound):
            self.__start(from_tag='9.9.9')

    def test_should_not_touch_master(self):
        before: str = self.git.rev_parse('master')
        self.__start(from_tag='1.29.0')
        self.assertEqual(before, self.git.rev_parse('master'))

    def test_should_refuse_when_tag_is_master_tip(self):
        LocalRepo.run(self.PATH, ['git', 'tag', '-a', '1.29.1', '-m', '1.29.1'])
        with self.assertRaises(TagIsMasterTip):
            self.__start(from_tag='1.29.1')

    def test_should_refuse_when_tag_state_version_disagrees(self):
        LocalRepo.run(self.PATH, ['git', 'checkout', '-qb', 'wrong', '1.29.0'])
        (self.PATH / 'flexio-flow.yml').write_text(
            'level: stable\nschemes: []\ntopics: []\nversion: 1.28.0\n')
        LocalRepo.run(self.PATH, ['git', 'commit', '-qam', 'hand made'])
        LocalRepo.run(self.PATH, ['git', 'tag', '-a', '1.27.0', '-m', '1.27.0'])
        LocalRepo.run(self.PATH, ['git', 'checkout', '-q', 'master'])
        with self.assertRaises(TagVersionMismatch):
            self.__start(from_tag='1.27.0')

    def test_should_refuse_a_tag_never_pushed(self):
        LocalRepo.with_remote(self.PATH)
        LocalRepo.run(self.PATH, ['git', 'tag', '-a', '1.29.2', '-m', '1.29.2', '1.29.0'])
        with self.assertRaises(TagNotPushed):
            self.__start(from_tag='1.29.2')
