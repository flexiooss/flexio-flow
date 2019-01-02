from __future__ import annotations
from VersionControl.VersionControl import VersionControl
from VersionControl.Branch import Branch
from VersionControl.GitFlow.Branches.BranchFactory import BranchFactory
from Branches.Branches import Branches


class GitFlow(VersionControl):

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
