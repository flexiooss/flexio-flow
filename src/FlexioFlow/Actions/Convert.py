from __future__ import annotations

from FlexioFlow.Options import Options
from Schemes.DevPrefix import DevPrefix
from Schemes.Schemes import Schemes
from typing import Dict


class Convert:

    def __init__(self,
                 options: Options,
                 ) -> None:
        self.options: Options = options

    def process(self):
        from_schemes: Schemes = self.options.from_schemes
        to_schemes: Schemes = self.options.to_schemes
        version: str = self.options.version
        if not version:
            raise ValueError('version is empty')

        print(version.replace(
            '-' + DevPrefix.from_schemes(from_schemes),
            '-' + DevPrefix.from_schemes(to_schemes)
        ))
