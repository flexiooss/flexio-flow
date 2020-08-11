from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option


class SchemeDir(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'scheme-dir'

    def exec(self) -> Options:
        self.options.scheme_dir = Path(str(self.arg))
        return self.options
