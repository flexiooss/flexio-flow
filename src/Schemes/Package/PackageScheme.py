from __future__ import annotations
from Schemes.Scheme import Scheme
from FlexioFlow.Version import Version
from Schemes.Package.PackageFileHandler import PackageFileHandler


class PackageScheme(Scheme):

    def set_version(self, version: Version) -> PackageScheme:
        p:PackageFileHandler = PackageFileHandler()

    def release_plan(self):
        pass
