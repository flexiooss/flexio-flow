from enum import Enum, unique
from typing import List, AnyStr, Dict
import re


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


class FlexioFlowConfig:
    version: str
    raw_version: Dict[int, int, int]
    level: Level = Level.STABLE
    scheme: List[Scheme]

    def __init__(self):
        pass

    @staticmethod
    def from_Dict(data: dict) -> FlexioFlowConfig:
        inst: FlexioFlowConfig = FlexioFlowConfig()
        if not inst.__match_version(data.version):
            raise ValueError('not version')
        inst.version = data.version

    @staticmethod
    def __match_version(version: AnyStr) -> bool:
        return re.compile('^\d+\.\d+\.d+$').match(version) >= 0

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def set_raw_version(self, major: int, minor: int, patch: int):
        self.raw_version.major = major
        self.raw_version.minor = minor
        self.raw_version.patch = patch
