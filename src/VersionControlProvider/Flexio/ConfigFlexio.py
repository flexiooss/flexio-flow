from __future__ import annotations
from typing import Dict, Optional, Union


class ConfigFlexio:

    def __init__(self, activate: bool, user_token: Optional[str], service_token: Optional[str]) -> None:
        self.__activate: bool = activate
        self.__user_token: Optional[str] = user_token
        self.__service_token: Optional[str] = service_token

    @property
    def user_token(self) -> Optional[str]:
        return self.__user_token

    @property
    def service_token(self) -> Optional[str]:
        return self.__service_token

    @property
    def activate(self) -> bool:
        return self.__activate

    def to_dict(self) -> Dict[str, Union[bool, str]]:
        return {
            'activate': self.activate,
            'user_token': str(self.__user_token) if self.__user_token is not None else '',
            'service_token': str(self.__service_token) if self.__service_token is not None else ''
        }
