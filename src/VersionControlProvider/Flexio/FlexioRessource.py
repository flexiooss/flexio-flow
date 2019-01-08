from __future__ import annotations
import abc


class FlexioRessource(abc.ABC):
    RESSOURCE_ID: str

    @abc.abstractmethod
    def __dict__(self):
        pass

    def to_api_dict(self) -> dict:
        ret: dict = self.__dict__()
        # ret['type_id'] = self.RESSOURCE_ID
        return ret
