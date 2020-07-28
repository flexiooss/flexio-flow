from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option


class Message(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'message'

    def exec(self) -> Options:
        self.options.message = self.arg
        return self.options
