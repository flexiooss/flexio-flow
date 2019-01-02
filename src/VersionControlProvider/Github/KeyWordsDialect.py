from VersionControlProvider.KeyWordsDialect import KeyWordsDialect as AbstractKeyWordsDialect


class KeyWordsDialect(AbstractKeyWordsDialect):

    @staticmethod
    def ref(self) -> str:
        return 'ref'

    @staticmethod
    def close(self) -> str:
        return 'close'
