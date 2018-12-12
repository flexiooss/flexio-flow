from __future__ import annotations

from FlexioFlow.Level import Level
from Schemes.Scheme import Scheme
from FlexioFlow.Version import Version
from Schemes.Package.PackageFileHandler import PackageFileHandler
from Schemes.Dependencies import Dependencies
from Schemes.Package.PreCheck import PreCheck


class PackageScheme(Scheme):

    @property
    def DEV_SUFFIX(self) -> str:
        return 'dev'

    def set_version(self) -> PackageScheme:
        package_handler: PackageFileHandler = PackageFileHandler(self.state_handler.dir_path)
        package_handler.set_version(
            str(self.state_handler.state.version) if self.state_handler.state.level is Level.STABLE else '-'.join(
                [str(self.state_handler.state.version), self.DEV_SUFFIX])
        ).write()
        return self

    def release_precheck(self) -> Dependencies:
        package_handler: PackageFileHandler = PackageFileHandler(self.state_handler.dir_path)
        release_precheck: PreCheck = PreCheck(package_handler, self.DEV_SUFFIX)
        return release_precheck.process()
