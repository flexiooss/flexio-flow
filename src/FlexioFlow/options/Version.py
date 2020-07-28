from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from Schemes.Schemes import Schemes


class Version(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'version'

    def exec(self) -> Options:
        self.options.version = self.clean_space(str(self.arg))
        return self.options
