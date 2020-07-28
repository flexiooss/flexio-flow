from __future__ import annotations
import abc
import re

from typing import List

from FlexioFlow.Options import Options


class Option(abc.ABC):
    arg: str = None
    opt: str = None
    HAS_VALUE: bool
    SHORT_NAME: str
    NAME: str

    def __init__(self, opt: str, arg: str, options: Options) -> None:
        self.opt: str = opt
        self.arg: str = arg
        self.options: Options = options

    def clean_space(self,txt: str) -> str:
        return re.sub('[\s+]', '', txt)

    def test(self) -> bool:
        options_name: List[str] = []
        if self.SHORT_NAME is not None:
            options_name.append('-' + self.SHORT_NAME)
        if self.NAME is not None:
            options_name.append('--' + self.NAME)
        return self.opt in options_name

    @abc.abstractmethod
    def exec(self) -> Options:
        pass

    @classmethod
    def process(cls, opt: str, arg: str, options: Options):
        option: Option = cls(opt, arg, options)
        if option.test():
            option.exec()
