from __future__ import annotations

from typing import List

from Log.Log import Log
from PoomCiDependency.Module import Module
from Schemes.Maven.MavenPreCheck import MavenPreCheck
from Schemes.Maven.MavenSetVersion import MavenSetVersion
from Schemes.Scheme import Scheme
from Schemes.Dependencies import Dependencies


class MavenScheme(Scheme):

    @property
    def DEV_SUFFIX(self) -> str:
        return 'SNAPSHOT'

    def set_version(self) -> MavenScheme:
        MavenSetVersion(self.state_handler, self.get_version()).set()
        return self

    def release_precheck(self) -> Dependencies:
        return MavenPreCheck(self.state_handler).check()

    def get_version(self) -> str:
        return '-'.join([self.state_handler.version_as_str(),
                         self.DEV_SUFFIX]) if self.state_handler.is_dev() else self.state_handler.version_as_str()

    def get_poom_ci_dependencies(self) -> List[Module]:
        Log.warning('Not implemented yet')

    def get_poom_ci_produces(self) -> List[Module]:
        Log.warning('Not implemented yet')
