from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option


class AutoStash(Option):
    HAS_VALUE = False
    SHORT_NAME = None
    NAME = 'auto-stash'

    def exec(self) -> Options:
        self.options.auto_stash = True
        return self.options
