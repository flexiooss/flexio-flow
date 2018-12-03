from typing import List
import re
from FlexioFlow.Scheme import Scheme
from FlexioFlow.Level import Level


class FlexioFlowValueObject:
    scheme: List[Scheme]

    def __init__(self, version: str, scheme: List[Scheme], level: Level) -> None:
        self.version = version
        self.scheme = scheme
        self.level = level

    @property
    def version(self) -> str:
        return self.__version

    @version.setter
    def version(self, v: str):
        if not self.match_version(v):
            raise ValueError('FlexioFlowValueObject.version should match ^\d+\.\d+\.\d+$')
        self.__version = v

    @staticmethod
    def match_version(version: str) -> bool:
        return re.compile('^\d+\.\d+\.\d+$').match(version) is not None

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    @property
    def level(self) -> Level:
        return self.__level

    @level.setter
    def level(self, v: Level):
        if not isinstance(v, Level):
            raise TypeError('level should be an instance of FlexioFlow.Level')
        self.__level = v

    @property
    def scheme(self) -> List[Scheme]:
        return self.__scheme

    @scheme.setter
    def scheme(self, v: List[Scheme]):
        if not (isinstance(item, Scheme) for item in v):
            raise TypeError('scheme should be an instance of List[FlexioFlow.Scheme]')
        self.__scheme = v

    def to_dict(self) -> dict:
        return {'version': self.version, 'level': self.level.value, 'scheme': self.schemeListValue(),
                }

    def schemeListValue(self) -> List[str]:
        ret = []
        for scheme in self.scheme:
            ret.append(scheme.value)
        return ret
