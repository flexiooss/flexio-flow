from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from Schemes.Schemes import Schemes


class RepositoryId(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'repository-id'

    def exec(self) -> Options:
        self.options.repository_id = self.clean_space(str(self.arg))
        return self.options
