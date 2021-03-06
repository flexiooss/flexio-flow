from Schemes.Composer.ComposerScheme import ComposerScheme
from Schemes.Maven.MavenScheme import MavenScheme
from Schemes.Schemes import Schemes
from Schemes.Scheme import Scheme
from Schemes.Package.PackageScheme import PackageScheme
from FlexioFlow.StateHandler import StateHandler


class SchemeBuilder:
    @staticmethod
    def create(scheme: Schemes, state_handler: StateHandler) -> Scheme:
        if scheme is Schemes.PACKAGE:
            return PackageScheme(state_handler)
        if scheme is Schemes.MAVEN:
            return MavenScheme(state_handler)
        if scheme is Schemes.COMPOSER:
            return ComposerScheme(state_handler)

        raise ValueError("Bad SchemeFactory creation: " + scheme.value)
