from Schemes.Schemes import Schemes
from typing import Type
from Schemes.Scheme import Scheme
from Schemes.Package.PackageScheme import PackageScheme
from FlexioFlow.StateHandler import StateHandler


class SchemeFactory:
    @staticmethod
    def create(scheme: Schemes, state_handler: StateHandler) -> Scheme:
        if scheme is Schemes.PACKAGE:
            return PackageScheme(state_handler)

        raise ValueError("Bad SchemeFactory creation: " + scheme.value)
