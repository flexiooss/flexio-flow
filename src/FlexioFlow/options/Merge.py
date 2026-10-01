from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option


class Merge(Option):
    HAS_VALUE = False
    SHORT_NAME = None
    NAME = 'merge'

    def exec(self) -> Options:
        self.options.merge = True
        return self.options
