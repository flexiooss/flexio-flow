from __future__ import annotations

from Schemes.Maven.MavenPreCheck import MavenPreCheck
from Schemes.Maven.MavenSetVersion import MavenSetVersion
from Schemes.Scheme import Scheme
from Schemes.Dependencies import Dependencies


class MavenScheme(Scheme):

    @property
    def DEV_SUFFIX(self) -> str:
        return 'SNAPSHOT'

    def set_version(self) -> MavenScheme:
        MavenSetVersion(self.__state_handler.dir_path.as_posix(), self.get_version()).set()
        return self

    def release_precheck(self) -> Dependencies:
        return MavenPreCheck(self.__state_handler.dir_path.as_posix()).check()

    def get_version(self) -> str:
        return '-'.join([self.state_handler.version_as_str(),
                           self.DEV_SUFFIX]) if self.state_handler.is_dev() else self.state_handler.version_as_str()
