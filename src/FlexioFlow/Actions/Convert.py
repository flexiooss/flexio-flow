from __future__ import annotations
from Schemes.DevPrefix import DevPrefix
from Schemes.Schemes import Schemes
from typing import Dict


class Convert:

    def __init__(self,
                 options: Dict[str, str],
                 ) -> None:
        self.options: Dict[str, str] = options

    def process(self):
        from_schemes: Schemes = Schemes.value_of(self.options.get('from'))
        to_schemes: Schemes = Schemes.value_of(self.options.get('to'))
        version: str = self.options.get('version')
        if not version:
            raise ValueError('version is empty')

        print(version.replace(
            '-' + DevPrefix.from_schemes(from_schemes),
            '-' + DevPrefix.from_schemes(to_schemes)
        ))
