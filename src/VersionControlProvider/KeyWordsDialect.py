from __future__ import annotations

import abc


class KeyWordsDialect(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def ref() -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def close() -> str:
        pass
