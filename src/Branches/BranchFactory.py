from Branches.Hotfix.Hotfix import Hotfix
from Branches.Release.Release import Release
from Branches.Branches import Branches
from Branches.Branch import Branch
from FlexioFlow.StateHandler import StateHandler

from typing import Type


class BranchFactory:
    @staticmethod
    def create(branch: Branches, state_handler: StateHandler) -> Branch:
        if branch is Branches.HOTFIX:
            return Hotfix(state_handler)
        if branch is Branches.RELEASE:
            return Release(state_handler)

        raise ValueError("Bad VersionFlowStepFactory creation: " + branch.value)
