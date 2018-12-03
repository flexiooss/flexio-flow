from enum import Enum, unique
from typing import List
import re
from pydantic.dataclasses import dataclass


@unique
class Level(Enum):
    DEV: str = 'dev'
    STABLE: str = 'stable'


@unique
class Scheme(Enum):
    MAVEN: str = 'maven'
    PACKAGE: str = 'package'
    COMPOSER: str = 'composer'
    DOCKER: str = 'docker'

@dataclass
class FlexioFlowValueObject:
    version: str
    level: Level = Level.STABLE
    scheme: List[Scheme]

    def __init__(self):
        pass

    @property
    def version(self) -> str:
        return self.version

    @version.setter
    def version(self, v: str):
        if not self.match_version(v):
            raise ValueError('FlexioFlowValueObject.version should match ^\d+\.\d+\.d+$')
        self.version = v

    @staticmethod
    def match_version(version: str) -> bool:
        return re.compile('^\d+\.\d+\.d+$').match(version) is not None

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
