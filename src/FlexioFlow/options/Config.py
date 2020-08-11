from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option


class Config(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'config'

    def exec(self) -> Options:
        self.options.config = self.clean_space(str(self.arg))
        return self.options
