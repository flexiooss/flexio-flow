from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option


class VersionDir(Option):
    HAS_VALUE = True
    SHORT_NAME = 'V'
    NAME = 'version-dir'

    def exec(self) -> Options:
        self.options.version_dir = Path(str(self.arg))
        return self.options
