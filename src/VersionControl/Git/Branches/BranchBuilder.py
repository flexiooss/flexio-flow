from VersionControl.Git.Branches.Develop.Develop import Develop
from VersionControl.Git.Branches.Feature.Feature import Feature
from VersionControl.Git.Branches.Hotfix.Hotfix import Hotfix
from VersionControl.Git.Branches.Release.Release import Release
from VersionControl.Git.Branches.Master.Master import Master

from Branches.Branches import Branches
from VersionControl.Branch import Branch
from FlexioFlow.StateHandler import StateHandler
from Core.ConfigHandler import ConfigHandler


class BranchBuilder:
    @staticmethod
    def create(branch: Branches, state_handler: StateHandler, config_handler: ConfigHandler) -> Branch:
        if branch is Branches.DEVELOP:
            return Develop(state_handler, config_handler)
        if branch is Branches.FEATURE:
            return Feature(state_handler, config_handler)
        if branch is Branches.HOTFIX:
            return Hotfix(state_handler, config_handler)
        if branch is Branches.MASTER:
            return Master(state_handler, config_handler)
        if branch is Branches.RELEASE:
            return Release(state_handler, config_handler)

        raise ValueError("Bad VersionFlowStepFactory creation: " + branch.value)
