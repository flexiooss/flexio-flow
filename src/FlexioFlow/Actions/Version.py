from __future__ import annotations
from Schemes.Scheme import Scheme
from Schemes.SchemeFactory import SchemeFactory
from Schemes.Schemes import Schemes
from typing import Optional, Type
from FlexioFlow.Actions.Action import Action


class Version(Action):

    def process(self):
        schemes: Optional[Schemes] = self.options.get('scheme')
        if schemes:
            scheme: Type[Scheme] = SchemeFactory.create(scheme=schemes, state_handler=self.state_handler)
            return print(scheme.get_version())
        else:
            return print(self.state_handler.version_as_str())
