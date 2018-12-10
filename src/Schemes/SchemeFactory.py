from Schemes.Schemes import Schemes
from typing import Type
from Schemes.Scheme import Scheme
from Schemes.Package.PackageScheme import PackageScheme


class SchemeFactory:
    @staticmethod
    def create(scheme: Schemes) -> Scheme:
        if scheme is Schemes.PACKAGE:
            return PackageScheme()

        raise ValueError("Bad SchemeFactory creation: " + scheme.value)
