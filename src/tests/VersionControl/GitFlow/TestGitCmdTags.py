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
