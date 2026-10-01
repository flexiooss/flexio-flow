from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option


class FromTag(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'from-tag'

    def exec(self) -> Options:
        self.options.from_tag = self.clean_space(str(self.arg))
        return self.options
