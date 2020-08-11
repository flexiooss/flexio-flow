from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from Schemes.Schemes import Schemes


class Read(Option):
    HAS_VALUE = False
    SHORT_NAME = 'R'
    NAME = 'read'

    def exec(self) -> Options:
        self.options.read = True
        return self.options
