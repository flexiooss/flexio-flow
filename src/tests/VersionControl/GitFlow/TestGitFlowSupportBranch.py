import unittest
from pathlib import Path

from Branches.BranchesConfig import BranchesConfig
from Core.Config import Config
from Core.ConfigHandler import ConfigHandler
from Exceptions.AmbiguousTagAtHead import AmbiguousTagAtHead
from Exceptions.NoChangesInBranch import NoChangesInBranch
from Exceptions.NoTagAtHead import NoTagAtHead
from Exceptions.TagIsMasterTip import TagIsMasterTip
from Exceptions.TagNotFound import TagNotFound
from Exceptions.TagNotPushed import TagNotPushed
from Exceptions.TagVersionMismatch import TagVersionMismatch
from FlexioFlow.Options import Options
from FlexioFlow.StateHandler import StateHandler
from VersionControl.Git.Branches.SupportBranch.Finish import Finish
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

    def __finish(self, merge=None) -> None:
        options: Options = Options()
        options.merge = merge
        Finish(
            state_handler=self.state_handler,
            config_handler=self.config_handler,
            issue=None,
            topics=None,
            keep_branch=False,
            close_issue=False,
            options=options
        ).process()

    def __fix(self, content: str, message: str) -> None:
        (self.PATH / 'f.txt').write_text(content)
        LocalRepo.run(self.PATH, ['git', 'commit', '-qam', message])

    def test_should_tag_on_support_branch_and_leave_master_alone(self):
        master_before: str = self.git.rev_parse('master')
        self.__start(from_tag='1.29.0')
        self.__fix('l1\nl2\nFIX\nl4\nl5\n', 'fix')
        self.__finish(merge=False)
        self.assertTrue(self.git.local_tag_exists('1.29.0.1'))
        self.assertEqual(master_before, self.git.rev_parse('master'))

    def test_should_leave_develop_untouched_with_no_merge(self):
        develop_before: str = self.git.rev_parse('develop')
        self.__start(from_tag='1.29.0')
        self.__fix('l1\nl2\nFIX\nl4\nl5\n', 'fix')
        self.__finish(merge=False)
        self.assertEqual(develop_before, self.git.rev_parse('develop'))

    def test_should_delete_the_support_branch(self):
        self.__start(from_tag='1.29.0')
        self.__fix('l1\nl2\nFIX\nl4\nl5\n', 'fix')
        self.__finish(merge=False)
        self.assertNotIn('support/1.29.0.1-dev', LocalRepo.run(self.PATH, ['git', 'branch', '--list']))

    def test_should_refuse_a_support_branch_with_no_fix(self):
        self.__start(from_tag='1.29.0')
        with self.assertRaises(NoChangesInBranch):
            self.__finish(merge=False)

    def test_should_refuse_when_no_merge_choice_given(self):
        self.__start(from_tag='1.29.0')
        self.__fix('l1\nl2\nFIX\nl4\nl5\n', 'fix')
        with self.assertRaises(ValueError):
            self.__finish(merge=None)
