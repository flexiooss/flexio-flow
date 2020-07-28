from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from Schemes.Schemes import Schemes


class To(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'to'

    def exec(self) -> Options:
        self.options.to_schemes = Schemes.value_of((self.clean_space(str(self.arg))))
        return self.options
