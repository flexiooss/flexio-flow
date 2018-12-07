from __future__ import annotations
from typing import List


class Dependencies:
    def __init__(self):
        self.__current = 0
        self.__list: list = []

    @staticmethod
    def from_list(dependencies: List[List[str]]) -> Dependencies:
        inst: Dependencies = Dependencies()
        for dep in dependencies:
            inst.append(dep[0], dep[1])
        return inst

    def append(self, dep_id: str, version: str) -> Dependencies:
        self.__list.append((dep_id, version))
        return self

    def __iter__(self):
        return self

    def __next__(self):
        if self.__current > self.__list.count():
            raise StopIteration
        else:
            self.__current += 1
            return self.__list[self.__current - 1]

    def __len__(self):
        return len(self.__list)
