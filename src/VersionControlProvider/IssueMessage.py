from __future__ import annotations

from typing import Optional, Type

import abc

from VersionControlProvider.Issue import Issue
from VersionControlProvider.KeyWordsDialect import KeyWordsDialect


class IssueMessage(abc.ABC):
    def __init__(self, message: str, issue: Optional[Type[Issue]] = None):
        self.message: str = message
        self.issue: Optional[Type[Issue]] = issue

    @staticmethod
    @abc.abstractmethod
    def keywords_dialect() -> Type[KeyWordsDialect]:
        pass

    def with_close(self) -> str:
        if self.issue is not None:
            return """{message!s} 
            
{close_keyword!s} {issue_ref!s}""".format(
                message=self.message,
                close_keyword=self.keywords_dialect().close(),
                issue_ref=self.issue.get_ref()
            )
        else:
            return self.message

    def with_ref(self) -> str:
        if self.issue is not None:
            return """{message!s} 
            
{ref_keyword!s} {issue_ref!s}""".format(
                message=self.message,
                ref_keyword=self.keywords_dialect().ref(),
                issue_ref=self.issue.get_ref()
            )
        else:
            return self.message
