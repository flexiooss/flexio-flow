from __future__ import annotations
from enum import Enum, unique
from typing import List

@unique
class Schemes(Enum):
    MAVEN: str = 'maven'
    PACKAGE: str = 'package'
    COMPOSER: str = 'composer'
    DOCKER: str = 'docker'

    @classmethod
    def list_from_value(cls, v: List[str]) -> List[Schemes]:
        ret = []
        for item in cls:
            if item.value in v:
                ret.append(item)

        return ret
