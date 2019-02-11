from __future__ import annotations

from VersionControlProvider.Flexio.FlexioRessource import FlexioRessource
from VersionControlProvider.IssueState import IssueState
from VersionControlProvider.Topic import Topic


class FlexioTopic(Topic, FlexioRessource):
    RESOURCE_ID: str = '5c336c70f3bb2517591449ab'
    RECORD_ID: str = '_id'
    NUMBER_ID: str = '5c336cebf3bb2517583dac83'
    TITLE_ID: str = '5c336c7ff3bb2517583dac61'
    BODY_ID: str = '5c337a75f3bb251c3d227691'
    STATE_ID: str = '5c337a44f3bb252171367670'
    SLUG: str = 'topic'

    def __state_to_value(self) -> str:
        if self.state is IssueState.OPEN:
            return '1'
        elif self.state is IssueState.CLOSED:
            return '0'
        return ''

    def __body_to_value(self) -> str:
        return self.body if self.body is not None else ''

    def url(self) -> str:
        return '{base_url!s}/{slug!s}/edit/{record_id!s}'.format(
            base_url=self.BASE_URL,
            slug=self.SLUG,
            record_id=self.id
        )

    def __dict__(self):
        ret: dict = {
            self.TITLE_ID: self.title,
            self.STATE_ID: self.__state_to_value(),
            self.BODY_ID: self.__body_to_value()
        }
        if self.number is not None:
            ret[self.NUMBER_ID] = self.number
        if self.id is not None:
            ret[self.RECORD_ID] = self.id
        return ret

    @classmethod
    def build_from_api(cls, json: dict) -> FlexioTopic:
        print(json)
        topic: FlexioTopic = FlexioTopic()
        topic._id = json.get(cls.RECORD_ID)
        topic.number = json.get(cls.NUMBER_ID)
        topic.title = json.get(cls.TITLE_ID)
        topic.body = json.get(cls.BODY_ID)
        topic.state = IssueState.OPEN if json.get(cls.STATE_ID) == '1' else IssueState.CLOSED
        return topic
