from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from Schemes.Schemes import Schemes


class Major(Option):
    HAS_VALUE = False
    SHORT_NAME = 'M'
    NAME = 'major'

    def exec(self) -> Options:
        self.options.major = True
        return self.options
