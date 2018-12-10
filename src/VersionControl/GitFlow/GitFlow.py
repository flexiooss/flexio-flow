from __future__ import annotations
from VersionControl.VersionControl import VersionControl
from VersionControl.Branch import Branch
from typing import Type
from VersionControl.GitFlow.Branches.BranchFactory import BranchFactory
from VersionControl.Branches import Branches


class GitFlow(VersionControl):
    def hotfix(self) -> Branch:
        branch: Branch = BranchFactory.create(Branches.HOTFIX, self.state_handler)
        return branch

    def release(self) -> Branch:
        branch: Branch = BranchFactory.create(Branches.RELEASE, self.state_handler)
        return branch

    def with_branch(self, branch: Branches) -> Branch:
        branch: Branch = BranchFactory.create(branch, self.state_handler)
        return branch
