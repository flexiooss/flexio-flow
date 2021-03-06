from __future__ import annotations

from typing import List, Dict, Any
from Schemes.Schemes import Schemes
from FlexioFlow.Level import Level
from FlexioFlow.Version import Version
from VersionControlProvider.DefaultTopic import DefaultTopic


class State:
    __version: Version
    __level: Level
    __schemes: List[Schemes]
    __topics: List[DefaultTopic]

    def __init__(self) -> None:
        self.__issues = []

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

    @property
    def topics(self) -> List[DefaultTopic]:
        return self.__topics

    @topics.setter
    def topics(self, v: List[DefaultTopic]):
        self.__topics: List[DefaultTopic] = v

    def to_dict(self) -> Dict[str, Any]:
        return {
            'version': str(self.version),
            'level': self.level.value,
            'schemes': self.__schemeListValue(),
            'topics': self.__topicNumberValue()
        }

    def next_major(self) -> Version:
        self.__version = self.__version.next_major()
        return self.__version

    def next_minor(self) -> Version:
        self.__version = self.__version.next_minor()
        return self.__version

    def next_patch(self) -> Version:
        self.__version = self.__version.next_patch()
        return self.__version

    def next_dev_patch(self) -> Version:
        self.__level = Level.DEV
        self.__version = self.__version.next_patch()
        return self.__version

    def next_dev_minor(self) -> Version:
        self.__level = Level.DEV
        self.__version = self.__version.next_minor()
        return self.__version

    def set_stable(self) -> State:
        self.__level = Level.STABLE
        return self

    def set_dev(self) -> State:
        self.__level = Level.DEV
        return self

    def __schemeListValue(self) -> List[str]:
        ret = []
        for scheme in self.schemes:
            ret.append(scheme.value)
        return ret

    def __topicNumberValue(self) -> List[int]:
        ret = []
        if self.__topics is not None:
            for topic in self.__topics:
                ret.append(topic.number)
        return ret

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
