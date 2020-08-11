from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from Schemes.Schemes import Schemes


class From(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'from'

    def exec(self) -> Options:
        self.options.from_schemes = Schemes.value_of((self.clean_space(str(self.arg))))
        return self.options
