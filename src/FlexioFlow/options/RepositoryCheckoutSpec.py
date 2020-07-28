from pathlib import Path

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from Schemes.Schemes import Schemes


class RepositoryCheckoutSpec(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'repository-checkout-spec'

    def exec(self) -> Options:
        self.options.repository_checkout_spec = self.clean_space(str(self.arg))
        return self.options
