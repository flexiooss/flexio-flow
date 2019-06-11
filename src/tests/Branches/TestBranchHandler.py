import unittest
from typing import Optional, List

from Branches.BranchHandler import BranchHandler
from Branches.Branches import Branches


class TestBranchHandler(unittest.TestCase):

    def test_topics(self):
        branch_handler: BranchHandler = BranchHandler(Branches.DEVELOP)
        numbers: Optional[List[int]] = branch_handler.topics_number_from_branch_name('feature/toto-tutu_1.4.0##52##12#2')
        print(numbers)
        self.assertEqual(numbers, [52,12])
        numbers: Optional[List[int]] = branch_handler.topics_number_from_branch_name('feature/toto-tutu_1.4.0#2')
        print(numbers)
        self.assertEqual(numbers, None)

    def test_issue(self):
        branch_handler: BranchHandler = BranchHandler(Branches.DEVELOP)
        numbers: Optional[List[int]] = branch_handler.issue_number_from_branch_name('feature/toto-tutu_1.4.0##52##12#2')
        print(numbers)
        self.assertEqual(numbers, 2)
        numbers: Optional[List[int]] = branch_handler.issue_number_from_branch_name('feature/toto-tutu_1.4.0##52##12')
        print('numbers')
        print(numbers)
        self.assertEqual(numbers, None)
