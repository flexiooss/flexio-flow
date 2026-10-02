from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option


class NoMerge(Option):
    HAS_VALUE = False
    SHORT_NAME = None
    NAME = 'no-merge'

    def exec(self) -> Options:
        self.options.merge = False
        return self.options
