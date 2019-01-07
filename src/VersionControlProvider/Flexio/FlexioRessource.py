from __future__ import annotations
import abc


class FlexioRessource(abc.ABC):
    RESSOURCE_ID: str

    @abc.abstractmethod
    def __dict__(self):
        pass

    def to_api_dict(self) -> dict:
        return self.__dict__()
