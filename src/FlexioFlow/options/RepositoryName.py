from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from Schemes.Schemes import Schemes


class RepositoryName(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'repository-name'

    def exec(self) -> Options:
        self.options.repository_name = self.clean_space(str(self.arg))
        return self.options
