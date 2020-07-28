from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from Schemes.Schemes import Schemes


class Scheme(Option):
    HAS_VALUE = True
    SHORT_NAME = 'S'
    NAME = 'scheme'

    def exec(self) -> Options:
        self.options.scheme = Schemes[str(self.arg).upper()]
        return self.options
