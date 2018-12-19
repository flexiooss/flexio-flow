from __future__ import annotations
from typing import Dict, Optional


class ConfigGithub:

    def __init__(self, activate: bool, user: Optional[str], token: Optional[str]) -> None:
        self.__activate: bool = activate
        self.__user: Optional[str] = user
        self.__token: Optional[str] = token

    @property
    def user(self) -> Optional[str]:
        return self.__user

    @property
    def token(self) -> Optional[str]:
        return self.__token

    @property
    def activate(self) -> bool:
        return self.__activate

    def to_dict(self) -> Dict[str, str]:
        return {
            'activate': self.activate,
            'user': self.user,
            'token': self.token
        }
