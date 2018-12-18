from __future__ import annotations

from pathlib import Path
from subprocess import Popen, PIPE
from typing import Dict, Optional, List

import requests
from requests import Response


class Github:
    BASE_URL: str = 'https://api.github.com'
    token: Optional[str]

    def __init__(self, dir_path: Path):
        self.token = None
        self.dir_path: Path = dir_path

    #
    # def __exec(self, args: List[str]):
    #     Popen(args, cwd=self.dir_path.as_posix()).communicate()
    #
    # def __exec_for_stdout(self, args: List[str]) -> str:
    #     stdout, stderr = Popen(args, stdout=PIPE, cwd=self.dir_path.as_posix()).communicate()
    #     return stdout.strip().decode('utf-8')

    def with_token(self, token: str) -> Github:
        inst: Github = Github(self.dir_path)
        inst.token = token
        return inst

    def get_user(self) -> Response:
        url: str = '/'.join([self.BASE_URL, 'user'])
        headers: Dict[str, str] = {}
        if self.token:
            headers['Authorization'] = 'token ' + self.token
            # headers['Authorization'] = 'token %s' % self.token
            r: Response = requests.get(url, headers=headers)
            print(r.status_code)
            print(r.json())
            return r

        else:
            raise AttributeError('No user or token')
