from __future__ import annotations

from typing import List, Dict, Any
from Schemes.Schemes import Schemes
from FlexioFlow.Level import Level
from FlexioFlow.Version import Version


class State:
    __version: Version
    __schemes: List[Schemes]

    def __init__(self) -> None:
        pass

    @property
    def version(self) -> Version:
        return self.__version

    @version.setter
    def version(self, v: Version):
        self.__version: Version = v

    @property
    def level(self) -> Level:
        return self.__level

    @level.setter
    def level(self, v: Level):
        if not isinstance(v, Level):
            raise TypeError('level should be an instance of FlexioFlow.Level')
        self.__level = v

    @property
    def schemes(self) -> List[Schemes]:
        return self.__schemes

    @schemes.setter
    def schemes(self, v: List[Schemes]):
        if not (isinstance(item, Schemes) for item in v):
            raise TypeError('schemes should be an instance of List[FlexioFlow.Scheme]')
        self.__schemes = v

    def to_dict(self) -> Dict[str, Any]:
        return {
            'version': str(self.version),
            'level': self.level.value,
            'schemes': self.__schemeListValue()
        }

    def next_major(self) -> Version:
        self.__version = self.__version.next_major()
        return self.__version

    def next_minor(self) -> Version:
        self.__version = self.__version.next_minor()
        return self.__version

    def next_patch(self) -> Version:
        self.__version = self.__version.next_minor()
        return self.__version

    def reset_patch(self) -> Version:
        self.__version = self.__version.reset_patch()
        return self.__version

    def __schemeListValue(self) -> List[str]:
        ret = []
        for scheme in self.schemes:
            ret.append(scheme.value)
        return ret

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
