#! /usr/bin/env python3
from ConsoleColors.PrintColor import PrintColor
import sys
from ConsoleColors.Fg import Fg
from Exceptions.GitMergeConflictError import GitMergeConflictError
from FlexioFlow.FlexioFlow import FlexioFlow
from pathlib import Path

from VersionControlProvider.Flexio.FlexioRequestApiError import FlexioRequestApiError
from VersionControlProvider.Github.GithubRequestApiError import GithubRequestApiError
from Executor import Executor


def main(argv) -> None:
    executor: Executor = Executor(Path.cwd()).exec(argv)

    flexio_flow: FlexioFlow = FlexioFlow(executor.config())

    if executor.config().options.debug:
        flexio_flow.process()
    else:
        try:
            flexio_flow.process()
        except KeyboardInterrupt:
            PrintColor.log(Fg.FOCUS.value + "\n\n" + '###  Flex bye bye budy !  ###' + "\n")
        except (
                FileNotFoundError, FileExistsError, ImportError, AttributeError, ValueError, KeyError,
                NotImplementedError,
                GitMergeConflictError, NotADirectoryError, TypeError, IndexError, GithubRequestApiError,
                ConnectionError,
                FlexioRequestApiError) as error:
            sys.stderr.write("""

{red}#######################################
# OUPS !!!
# {type}:{error}
#######################################{reset}

""".format(red=Fg.FAIL.value, type=error.__class__.__name__, error=error, reset=Fg.RESET.value))
            sys.stderr.write("Command terminated with wrong status code: 1" + "\n")
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
