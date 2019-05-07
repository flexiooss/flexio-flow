from __future__ import annotations
import abc


class FlexioRessource(abc.ABC):
    RESOURCE_ID: str
    SLUG: str
    BASE_URL: str = 'https://my.flexio.io/informations'
    id: str = None

    @abc.abstractmethod
    def __dict__(self):
        pass

    def to_api_dict(self) -> dict:
        ret: dict = self.__dict__()
        # ret['type_id'] = self.RESOURCE_ID
        return ret

    def with_id(self, id: str) -> FlexioRessource:
        self.id = id
        return self

    @classmethod
    @abc.abstractmethod
    def build_from_api(cls, json: dict) -> FlexioRessource:
        pass
