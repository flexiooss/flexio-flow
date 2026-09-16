from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option


class BranchName(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'branch-name'

    def exec(self) -> Options:
        self.options.branch_name = self.arg
        return self.options
