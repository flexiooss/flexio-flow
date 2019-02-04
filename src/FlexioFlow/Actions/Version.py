from __future__ import annotations

from FlexioFlow.StateHandler import StateHandler
from Schemes.Scheme import Scheme
from Schemes.SchemeFactory import SchemeFactory
from Schemes.Schemes import Schemes
from typing import Optional, Type, Dict


class Version:

    def __init__(self,
                 state_handler: StateHandler,
                 options: Dict[str, str],
                 ) -> None:
        self.state_handler: StateHandler = state_handler
        self.options: Dict[str, str] = options

    def __get_scheme_option_or_default(self) -> Optional[Schemes]:
        schemes: Optional[Schemes] = self.options.get('scheme')
        if schemes is None:
            schemes = self.state_handler.first_scheme()
        return schemes


    def process(self):
        schemes: Optional[Schemes] = self.__get_scheme_option_or_default()

        if schemes:
            scheme: Type[Scheme] = SchemeFactory.create(
                scheme=schemes,
                state_handler=self.state_handler
            )
            return print(scheme.get_version())
        else:
            return print(self.state_handler.version_as_str())
