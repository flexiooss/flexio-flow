from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from Schemes.Schemes import Schemes


class Default(Option):
    HAS_VALUE = False
    SHORT_NAME = 'D'
    NAME = 'default'

    def exec(self) -> Options:
        self.options.default = True
        return self.options
