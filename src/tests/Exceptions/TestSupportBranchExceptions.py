import unittest

from Exceptions.AmbiguousTagAtHead import AmbiguousTagAtHead
from Exceptions.MergeCommitBetweenBounds import MergeCommitBetweenBounds
from Exceptions.NoTagAtHead import NoTagAtHead
from Exceptions.TagIsMasterTip import TagIsMasterTip
from Exceptions.TagNotFound import TagNotFound
from Exceptions.TagNotPushed import TagNotPushed
from Exceptions.TagVersionMismatch import TagVersionMismatch


class TestSupportBranchExceptions(unittest.TestCase):

    def test_tag_not_found_names_the_tag_and_the_known_ones(self):
        message: str = str(TagNotFound('1.29.0', ['1.28.0', '1.29.1']))
        self.assertIn('1.29.0', message)
        self.assertIn('1.29.1', message)

    def test_tag_not_pushed_tells_to_push(self):
        message: str = str(TagNotPushed('1.29.0'))
        self.assertIn('1.29.0', message)
        self.assertIn('push', message)

    def test_no_tag_at_head_tells_the_option(self):
        self.assertIn('--from-tag', str(NoTagAtHead()))

    def test_ambiguous_tag_lists_candidates(self):
        message: str = str(AmbiguousTagAtHead(['1.29.0', '1.30.0']))
        self.assertIn('1.29.0', message)
        self.assertIn('1.30.0', message)
        self.assertIn('--from-tag', message)

    def test_tag_version_mismatch_shows_both(self):
        message: str = str(TagVersionMismatch('1.29.0', '1.28.0'))
        self.assertIn('1.29.0', message)
        self.assertIn('1.28.0', message)

    def test_merge_commit_tells_to_finish_without_merge(self):
        self.assertIn('--no-merge', str(MergeCommitBetweenBounds('support/1.29.0.1-dev')))

    def test_tag_is_master_tip_sends_back_to_hotfix(self):
        message: str = str(TagIsMasterTip('1.29.0'))
        self.assertIn('1.29.0', message)
        self.assertIn('hotfix', message)
