from __future__ import annotations
from VersionControlProvider.Topic import Topic


class DefaultTopic(Topic):

    def __dict__(self):
        return {
            'number': self.number
        }

    def url(self) -> str:
        return 'no url for default'

    def get_ref(self) -> str:
        if self.number is None:
            raise ValueError('Topic should have a number')
        return '{prefix!s}{number!s}'.format(prefix=self.PREFIX, number=self.number)

    def to_dict(self) -> dict:
        return {
            'number': self.number,
            'title': self.title,
            'body': self.body,
            'url': self.url()
        }
