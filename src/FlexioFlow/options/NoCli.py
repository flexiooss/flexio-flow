from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from Schemes.Schemes import Schemes


class NoCli(Option):
    HAS_VALUE = False
    SHORT_NAME = 'N'
    NAME = 'no-cli'

    def exec(self) -> Options:
        self.options.no_cli = True
        return self.options
