import unittest
from pathlib import Path

from FlexioFlow.StateHandler import StateHandler
from VersionControl.Git.GitCmd import GitCmd
from tests.VersionControl.GitFlow.LocalRepo import LocalRepo


class TestGitCmdTags(unittest.TestCase):
    PATH: Path = Path('/tmp/test_flexioflow_tags')

    def setUp(self):
        LocalRepo.create(self.PATH)
        self.git: GitCmd = GitCmd(state_handler=StateHandler(self.PATH))

    def tearDown(self):
        LocalRepo.clean(self.PATH)
        LocalRepo.clean(Path(self.PATH.as_posix() + '_remote.git'))

    def test_should_find_tag_when_alone(self):
        self.assertTrue(self.git.local_tag_exists('1.29.0'))

    def test_should_find_tag_when_another_tag_has_it_as_prefix(self):
        LocalRepo.run(self.PATH, ['git', 'tag', '-a', '1.29.0.1', '-m', '1.29.0.1'])
        self.assertTrue(self.git.local_tag_exists('1.29.0'))
        self.assertTrue(self.git.local_tag_exists('1.29.0.1'))

    def test_should_not_find_absent_tag(self):
        self.assertFalse(self.git.local_tag_exists('9.9.9'))

    def test_should_not_match_dot_as_wildcard(self):
        LocalRepo.run(self.PATH, ['git', 'tag', '-a', '1x29x0', '-m', 'x'])
        LocalRepo.run(self.PATH, ['git', 'tag', '-d', '1.29.0'])
        self.assertFalse(self.git.local_tag_exists('1.29.0'))

    def test_should_find_annotated_tag_on_remote(self):
        LocalRepo.with_remote(self.PATH)
        self.assertTrue(self.git.remote_tag_exists('1.29.0'))

    def test_should_not_find_unpushed_tag_on_remote(self):
        LocalRepo.with_remote(self.PATH)
        LocalRepo.run(self.PATH, ['git', 'tag', '-a', '1.29.0.1', '-m', '1.29.0.1'])
        self.assertFalse(self.git.remote_tag_exists('1.29.0.1'))

    def test_should_not_match_dot_as_wildcard_on_remote(self):
        LocalRepo.run(self.PATH, ['git', 'tag', '-a', '1x29x0', '-m', 'x'])
        LocalRepo.with_remote(self.PATH)
        LocalRepo.run(self.PATH, ['git', 'push', '-q', 'origin', ':refs/tags/1.29.0'])
        self.assertFalse(self.git.remote_tag_exists('1.29.0'))

    def test_should_create_branch_from_a_tag(self):
        self.git.create_branch_from_revision('support/1.29.0.1-dev', '1.29.0')
        self.assertEqual('support/1.29.0.1-dev', LocalRepo.run(self.PATH, ['git', 'branch', '--show-current']))

    def test_should_skip_fetch_when_no_remote(self):
        self.assertIs(self.git, self.git.try_to_fetch_tags())

    def __diverge_develop(self) -> None:
        LocalRepo.run(self.PATH, ['git', 'checkout', '-q', 'develop'])
        (self.PATH / 'other.txt').write_text('develop moved\n')
        LocalRepo.run(self.PATH, ['git', 'add', '.'])
        LocalRepo.run(self.PATH, ['git', 'commit', '-qm', 'develop moved'])
        LocalRepo.run(self.PATH, ['git', 'checkout', '-q', 'master'])

    def test_should_detect_merge_commit_between_bounds(self):
        self.__diverge_develop()
        base: str = self.git.rev_parse('master')
        LocalRepo.run(self.PATH, ['git', 'checkout', '-qb', 'work'])
        (self.PATH / 'f.txt').write_text('l1\nl2\nWORK\nl4\nl5\n')
        LocalRepo.run(self.PATH, ['git', 'commit', '-qam', 'work'])
        LocalRepo.run(self.PATH, ['git', 'merge', '-q', '--no-ff', '-m', 'merge', 'develop'])
        self.assertTrue(self.git.has_merge_commit_between(base, 'work'))

    def test_should_not_detect_merge_commit_on_linear_history(self):
        base: str = self.git.rev_parse('master')
        LocalRepo.run(self.PATH, ['git', 'checkout', '-qb', 'work'])
        (self.PATH / 'f.txt').write_text('l1\nl2\nWORK\nl4\nl5\n')
        LocalRepo.run(self.PATH, ['git', 'commit', '-qam', 'work'])
        self.assertFalse(self.git.has_merge_commit_between(base, 'work'))

    def test_should_find_first_commit_after_base(self):
        base: str = self.git.rev_parse('master')
        LocalRepo.run(self.PATH, ['git', 'checkout', '-qb', 'work'])
        (self.PATH / 'f.txt').write_text('one\n')
        LocalRepo.run(self.PATH, ['git', 'commit', '-qam', 'one'])
        first: str = self.git.rev_parse('work')
        (self.PATH / 'f.txt').write_text('two\n')
        LocalRepo.run(self.PATH, ['git', 'commit', '-qam', 'two'])
        self.assertEqual(first, self.git.first_commit_after(base, 'work'))

    def test_should_build_a_commit_tree_whose_diff_excludes_equal_files(self):
        LocalRepo.run(self.PATH, ['git', 'checkout', '-qb', 'work'])
        (self.PATH / 'flexio-flow.yml').write_text('version: 1.29.0.1\n')
        LocalRepo.run(self.PATH, ['git', 'commit', '-qam', 'bookkeeping'])
        low: str = self.git.rev_parse('work')
        (self.PATH / 'f.txt').write_text('FIX\n')
        LocalRepo.run(self.PATH, ['git', 'commit', '-qam', 'fix'])
        high: str = self.git.rev_parse('work')
        synthetic: str = self.git.commit_tree(self.git.tree_of(high), low, 'synthetic')
        changed: str = LocalRepo.run(self.PATH, ['git', 'diff', '--name-only', low, synthetic])
        self.assertEqual('f.txt', changed)
