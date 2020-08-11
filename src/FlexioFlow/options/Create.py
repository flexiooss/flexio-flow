from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from Schemes.Schemes import Schemes


class Create(Option):
    HAS_VALUE = False
    SHORT_NAME = 'C'
    NAME = 'create'

    def exec(self) -> Options:
        self.options.create = True
        return self.options
