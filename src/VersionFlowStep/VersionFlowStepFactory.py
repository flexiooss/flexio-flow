from VersionFlowStep import AbstractVersionFlowStep, Hotfix, Release
from FlexioFlow import VersionFlowStep


class VersionFlowStepFactory:
    @staticmethod
    def get(versionFlowStep: VersionFlowStep) -> AbstractVersionFlowStep:
        if versionFlowStep is VersionFlowStep.HOTFIX:
            return Hotfix()
        if versionFlowStep is VersionFlowStep.RELEASE:
            return Release()

        raise ValueError("Bad VersionFlowStepFactory creation: " + versionFlowStep)
