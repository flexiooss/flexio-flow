from __future__ import annotations
from Schemes.Scheme import Scheme
from FlexioFlow.Version import Version
from Schemes.Package.PackageFileHandler import PackageFileHandler


class PackageScheme(Scheme):

    def set_version(self) -> PackageScheme:
        package_handler: PackageFileHandler = PackageFileHandler(self.dir_path)
        package_handler.set_version(self.state.version).write()
        return self

    def release_plan(self):
        pass
