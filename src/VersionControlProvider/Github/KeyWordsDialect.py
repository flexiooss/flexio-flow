from VersionControlProvider.KeyWordsDialect import KeyWordsDialect as AbstractKeyWordsDialect


class KeyWordsDialect(AbstractKeyWordsDialect):

    @staticmethod
    def ref() -> str:
        return 'ref'

    @staticmethod
    def close() -> str:
        return 'close'
