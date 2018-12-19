from __future__ import annotations

from pathlib import Path
from subprocess import Popen, PIPE
from typing import Dict, Optional, List

import requests
from requests import Response

from Core.ConfigHandler import ConfigHandler


class Github:
    BASE_URL: str = 'https://api.github.com'

    def __init__(self, config_handler: ConfigHandler):
        self.config_handler: ConfigHandler = config_handler

    #
    # def __exec(self, args: List[str]):
    #     Popen(args, cwd=self.dir_path.as_posix()).communicate()
    #
    # def __exec_for_stdout(self, args: List[str]) -> str:
    #     stdout, stderr = Popen(args, stdout=PIPE, cwd=self.dir_path.as_posix()).communicate()
    #     return stdout.strip().decode('utf-8')
    def __auth(self, headers: Dict[str, str]) -> Dict[str, str]:
        if self.config_handler.config.github.token:
            headers['Authorization'] = 'token {github_token!s}'.format(
                github_token=self.config_handler.config.github.token)
        else:
            raise AttributeError('No user or token')
        return headers

    def get_user(self) -> Response:
        url: str = '/'.join([self.BASE_URL, 'user'])
        headers: Dict[str, str] = {}
        r: Response = requests.get(url, headers=self.__auth(headers))
        print(r.status_code)
        print(r.json())
        return r
