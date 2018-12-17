from typing import Optional

from FlexioFlow.Level import Level
from FlexioFlow.Version import Version
from VersionControl.Branches import Branches


class BranchHandler:
    @staticmethod
    def branch_name_from_version(branch: Branches, version: Optional[Version] = None) -> str:
        if branch is Branches.HOTFIX:
            return '/'.join([
                Branches.HOTFIX.value,
                '-'.join([str(version), Level.DEV.value])
            ])
        if branch is Branches.RELEASE:
            return '/'.join([Branches.RELEASE.value, str(version)])
        else:
            return branch.value
