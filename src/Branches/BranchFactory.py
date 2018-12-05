from Branches.Hotfix import Hotfix
from Branches.Release import Release
from Branches.Branches import Branches
from Branches.Branch import Branch
from typing import Type


class BranchFactory:
    @staticmethod
    def create(branch: Branches) -> Branch:
        if branch is Branches.HOTFIX:
            return Hotfix()
        if branch is Branches.RELEASE:
            return Release()

        raise ValueError("Bad VersionFlowStepFactory creation: " + branch.value)
