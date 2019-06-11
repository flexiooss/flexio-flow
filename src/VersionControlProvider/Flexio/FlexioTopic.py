from __future__ import annotations

from VersionControlProvider.Flexio.FlexioRessource import FlexioRessource
from VersionControlProvider.Topic import Topic


class FlexioTopic(Topic, FlexioRessource):
    RESOURCE_ID: str = '5c336c70f3bb2517591449ab'
    RECORD_ID: str = '_id'
    NUMBER_ID: str = '5c336cebf3bb2517583dac83'
    TITLE_ID: str = '5c336c7ff3bb2517583dac61'
    BODY_ID: str = '5c337a75f3bb251c3d227691'
    SLUG: str = 'topics'

    def __body_to_value(self) -> str:
        return self.body if self.body is not None else ''

    def url(self) -> str:
        return '{base_url!s}/{slug!s}/edit/{record_id!s}'.format(
            base_url=self.BASE_URL,
            slug=self.SLUG,
            record_id=self.id
        )

    def to_dict(self) -> dict:
        return {
            'number': self.number,
            'title': self.title,
            'body': self.body,
            'url': self.url()
        }

    def __dict__(self):
        ret: dict = {}
        if self.body is not None:
            ret[self.BODY_ID] = self.__body_to_value()
        if self.title is not None:
            ret[self.TITLE_ID] = self.title
        if self.number is not None:
            ret[self.NUMBER_ID] = self.number
        if self.id is not None:
            ret[self.RECORD_ID] = self.id
        return ret

    @classmethod
    def build_from_api(cls, json: dict) -> FlexioTopic:
        topic: FlexioTopic = FlexioTopic()
        topic.id = json.get(cls.RECORD_ID)
        topic.number = json.get(cls.NUMBER_ID)
        topic.title = json.get(cls.TITLE_ID)
        topic.body = json.get(cls.BODY_ID)
        return topic

    def get_ref(self) -> str:
        if self.number is None:
            raise ValueError('Topic should have a number')
        return '{prefix!s}{number!s}'.format(prefix=self.PREFIX, number=self.number)
