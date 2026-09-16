from __future__ import annotations

from typing import Callable

from ConsoleColors.Fg import Fg
from Exceptions.NoFeatureName import NoFeatureName
from FlexioFlow.Options import Options


class FeatureName:
    MISSING: str = 'Set it with --branch-name=<name> or run without --default / --no-cli'

    def __init__(self, options: Options, default_name: str = '', reader: Callable[[str], str] = input):
        self.__options: Options = options
        self.__default_name: str = default_name
        self.__reader: Callable[[str], str] = reader

    def __is_interactive(self) -> bool:
        return not self.__options.default and self.__options.no_cli is not True

    def __from_options(self) -> str:
        return self.__options.branch_name if self.__options.branch_name else ''

    def __from_cli(self) -> str:
        return self.__reader(
            Fg.FAIL.value + '[required]' + Fg.RESET.value + ' Feature branch name : ' + Fg.NOTICE.value + self.__default_name + Fg.RESET.value + ' ')

    def ensure_available(self) -> None:
        if not self.__from_options() and not self.__is_interactive():
            raise NoFeatureName(self.MISSING)

    def resolve(self) -> str:
        name: str = self.__from_options()

        if not name and self.__is_interactive():
            name = self.__from_cli()

        name = name if name else self.__default_name

        if not name:
            raise NoFeatureName(self.MISSING)

        return name
