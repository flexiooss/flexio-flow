from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option


class Debug(Option):
    HAS_VALUE = False
    SHORT_NAME = None
    NAME = 'debug'

    def exec(self) -> Options:
        self.options.debug = True
        return self.options
