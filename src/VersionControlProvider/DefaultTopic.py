from __future__ import annotations
from VersionControlProvider.Topic import Topic


class DefaultTopic(Topic):

    def __dict__(self):
        return {
            'number': self.number
        }

    def url(self) -> str:
        return 'no url for default'
