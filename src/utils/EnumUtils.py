from enum import Enum
from typing import List


class EnumUtils():
    def __init__(self, enum: Enum):
        if not issubclass(enum, Enum):
            raise TypeError('EnumUtils enums arg should be instance of Enum')
        self.__enum = enum

    def has_value(self, value) -> bool:
        return bool(any(value == item.value for item in self.__enum))

    def list_from_value(self, list: List[str]) -> List[Enum]:
        ret = []
        for item in self.__enum:
            if item.value in list:
                ret.append(item)

        return ret
