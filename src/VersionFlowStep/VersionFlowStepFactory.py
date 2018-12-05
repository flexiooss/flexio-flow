from VersionFlowStep.AbstractVersionFlowStep import AbstractVersionFlowStep
from VersionFlowStep.Hotfix import Hotfix
from VersionFlowStep.Release import Release
from FlexioFlow.VersionFlowStep import VersionFlowStep


class VersionFlowStepFactory:
    @staticmethod
    def create(versionFlowStep: VersionFlowStep) -> AbstractVersionFlowStep:
        if versionFlowStep is VersionFlowStep.HOTFIX:
            return Hotfix()
        if versionFlowStep is VersionFlowStep.RELEASE:
            return Release()

        raise ValueError("Bad VersionFlowStepFactory creation: " + versionFlowStep.value)
