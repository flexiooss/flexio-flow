from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from Schemes.Schemes import Schemes


class FileName(Option):
    HAS_VALUE = True
    SHORT_NAME = 'F'
    NAME = 'filename'

    def exec(self) -> Options:
        self.options.filename = self.clean_space(str(self.arg))
        return self.options
