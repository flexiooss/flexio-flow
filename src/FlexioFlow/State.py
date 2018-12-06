from __future__ import annotations

from typing import List, Dict, Any
from Schemes.Schemes import Schemes
from FlexioFlow.Level import Level
from FlexioFlow.Version import Version


class State:

    def __init__(self) -> None:
        pass

    @property
    def version(self) -> Version:
        return self.__version

    @version.setter
    def version(self, v: Version):
        self.__version = v

    @property
    def level(self) -> Level:
        return self.__level

    @level.setter
    def level(self, v: Level):
        if not isinstance(v, Level):
            raise TypeError('level should be an instance of FlexioFlow.Level')
        self.__level = v

    @property
    def scheme(self) -> List[Schemes]:
        return self.__scheme

    @scheme.setter
    def scheme(self, v: List[Schemes]):
        if not (isinstance(item, Schemes) for item in v):
            raise TypeError('scheme should be an instance of List[FlexioFlow.Scheme]')
        self.__scheme = v

    def to_dict(self) -> Dict[str, Any]:
        return {
            'version': str(self.version),
            'level': self.level.value,
            'scheme': self.__schemeListValue()
        }

    def __schemeListValue(self) -> List[str]:
        ret = []
        for scheme in self.scheme:
            ret.append(scheme.value)
        return ret

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
