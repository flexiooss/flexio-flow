from typing import Dict

import requests
from requests import Response

from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Flexio.FlexioRessource import FlexioRessource


class FlexioClient:
    BASE_URL: str = 'https://my.flexio.io/api'

    def __init__(self, config_handler: ConfigHandler):
        self.__config_handler: ConfigHandler = config_handler

    def __auth(self, headers: Dict[str, str]) -> Dict[str, str]:
        if self.__config_handler.config.flexio.service_token and self.__config_handler.config.flexio.user_token:
            headers['Authorization'] = 'Bearer {service_token!s}'.format(
                service_token=self.__config_handler.config.flexio.service_token)
            headers['X-user'] = '{user_token!s}'.format(
                user_token=self.__config_handler.config.flexio.user_token)
        else:
            raise AttributeError('No user or service token')
        return headers

    def post_record(self, record: FlexioRessource) -> Response:
        url: str = '/'.join([self.BASE_URL, 'record', record.RESSOURCE_ID])
        return requests.post(url, json=record.to_api_dict(), headers=self.__auth({}))

    # def get_user(self)->Response:
