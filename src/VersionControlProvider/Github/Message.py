from typing import Type

from VersionControlProvider.Github.KeyWordsDialect import KeyWordsDialect
from VersionControlProvider.KeyWordsDialect import KeyWordsDialect as AbstractKeyWordsDialect
from VersionControlProvider.Message import Message as AbstractMessage


class Message(AbstractMessage):
    def keywords_dialect(self) -> Type[AbstractKeyWordsDialect]:
        return KeyWordsDialect
