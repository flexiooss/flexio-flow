from typing import Type

from VersionControlProvider.Github.KeyWordsDialect import KeyWordsDialect
from VersionControlProvider.KeyWordsDialect import KeyWordsDialect as AbstractKeyWordsDialect
from VersionControlProvider.IssueMessage import IssueMessage as AbstractMessage


class Message(AbstractMessage):

    @staticmethod
    def keywords_dialect() -> Type[AbstractKeyWordsDialect]:
        return KeyWordsDialect
