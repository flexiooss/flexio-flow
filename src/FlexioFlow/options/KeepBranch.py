from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from Schemes.Schemes import Schemes


class KeepBranch(Option):
    HAS_VALUE = False
    SHORT_NAME = 'K'
    NAME = 'keep-branch'

    def exec(self) -> Options:
        self.options.keep_branch = True
        return self.options
