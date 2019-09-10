from Schemes.Composer.ComposerScheme import ComposerScheme
from Schemes.Maven.MavenScheme import MavenScheme
from Schemes.Package.PackageScheme import PackageScheme
from Schemes.Schemes import Schemes


class DevPrefix:

    @classmethod
    def from_schemes(cls, schemes: Schemes) -> str:
        if schemes == Schemes.MAVEN:
            return MavenScheme.DEV_SUFFIX
        if schemes == Schemes.PACKAGE:
            return PackageScheme.DEV_SUFFIX
        if schemes == Schemes.COMPOSER:
            return ComposerScheme.DEV_SUFFIX

        raise ValueError("Bad SchemeFactory creation: " + schemes.value)
