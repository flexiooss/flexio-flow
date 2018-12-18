from __future__ import annotations
import re
from typing import Dict, Match


class Config:

    def __init__(self, user: str, token: str) -> None:
        self.__user: str = user
        self.__token: str = token

    @property
    def user(self) -> str:
        return self.__user

    @property
    def token(self) -> str:
        return self.__token

    def to_dict(self) -> Dict[str, str]:
        return {
            'user': self.user,
            'token': self.token
        }
