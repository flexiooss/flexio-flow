from VersionControl.Git.Branches.Feature.Feature import Feature
from VersionControl.Git.Branches.Hotfix.Hotfix import Hotfix
from VersionControl.Git.Branches.Release.Release import Release
from VersionControl.Git.Branches.Master.Master import Master

from Branches.Branches import Branches
from VersionControl.Branch import Branch
from FlexioFlow.StateHandler import StateHandler


class BranchBuilder:
    @staticmethod
    def create(branch: Branches, state_handler: StateHandler) -> Branch:
        if branch is Branches.FEATURE:
            return Feature(state_handler)
        if branch is Branches.HOTFIX:
            return Hotfix(state_handler)
        if branch is Branches.MASTER:
            return Master(state_handler)
        if branch is Branches.RELEASE:
            return Release(state_handler)

        raise ValueError("Bad VersionFlowStepFactory creation: " + branch.value)
