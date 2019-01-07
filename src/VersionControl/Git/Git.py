from __future__ import annotations

from typing import Optional

from VersionControl.Git.IssueHandler import IssueHandler
from VersionControl.VersionControl import VersionControl
from VersionControl.Branch import Branch
from VersionControl.Git.Branches.BranchFactory import BranchFactory
from Branches.Branches import Branches


class Git(VersionControl):

    def build_branch(self, branch: Branches) -> Branch:
        branch_inst: Branch = BranchFactory.create(branch, self.state_handler)
        return branch_inst

    def feature(self) -> Branch:
        branch_inst: Branch = BranchFactory.create(Branches.FEATURE, self.state_handler)
        return branch_inst

    def hotfix(self) -> Branch:
        branch_inst: Branch = BranchFactory.create(Branches.HOTFIX, self.state_handler)
        return branch_inst

    def master(self) -> Branch:
        branch_inst: Branch = BranchFactory.create(Branches.MASTER, self.state_handler)
        return branch_inst

    def release(self) -> Branch:
        branch_inst: Branch = BranchFactory.create(Branches.RELEASE, self.state_handler)
        return branch_inst

    def get_issue_number(self) -> Optional[int]:
        issue_number: Optional[int] = IssueHandler(self.state_handler).number_from_branch_name()
        return issue_number

    def commit(self, message: str):
        print('commit')
        print(message)
