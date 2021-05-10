from __future__ import annotations
from typing import Dict, Optional, Union

from Branches.Branches import Branches


class BranchesConfig:

    def __init__(self, develop: Optional[str], feature: Optional[str], hotfix: Optional[str], master: Optional[str],
                 release: Optional[str]) -> None:
        self.__develop = Branches.DEVELOP.value if develop is None else develop
        self.__feature = Branches.FEATURE.value if feature is None else feature
        self.__hotfix = Branches.HOTFIX.value if hotfix is None else hotfix
        self.__master = Branches.MASTER.value if master is None else master
        self.__release = Branches.RELEASE.value if release is None else release

    @staticmethod
    def from_dict(branches: Optional[dict]) -> BranchesConfig:
        return BranchesConfig(
            develop=branches.get('develop', None),
            feature=branches.get('feature', None),
            hotfix=branches.get('hotfix', None),
            master=branches.get('master', None),
            release=branches.get('release', None)
        )

    @property
    def develop(self) -> str:
        return self.__develop

    def is_develop(self, name: str) -> bool:
        return name is self.develop

    @property
    def feature(self) -> str:
        return self.__feature

    def is_feature(self, name: str) -> bool:
        return name is self.feature

    @property
    def hotfix(self) -> str:
        return self.__hotfix

    def is_hotfix(self, name: str) -> bool:
        return name is self.hotfix

    @property
    def master(self) -> str:
        return self.__master

    def is_master(self, name: str) -> bool:
        return name is self.master

    @property
    def release(self) -> str:
        return self.__release

    def is_release(self, name: str) -> bool:
        return name is self.release

    def to_dict(self) -> Dict[str, str]:
        return {
            'develop': self.develop,
            'feature': self.feature,
            'hotfix': self.hotfix,
            'master': self.master,
            'release': self.release,
        }
