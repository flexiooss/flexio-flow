from subprocess import Popen, PIPE
from typing import Optional, List

from requests import Response

from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Github.ConfigGithub import ConfigGithub
from VersionControlProvider.Github.Github import Github


class InputConfig:
    def __init__(self, config_handler: ConfigHandler):
        self.config_handler: ConfigHandler = config_handler

    def __exec_for_stdout(self, args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE, cwd=self.config_handler.dir_path.as_posix()).communicate()
        return stdout.strip().decode('utf-8')

    def __input_github(self) -> bool:
        if self.config_handler.has_issuer():
            github: str = input('Activate Github automatic issuer (y)/n : ')
            github = github if github else 'y'
        else:
            github: str = input('Activate Github automatic issuer y/(n) : ')
            github = github if github else 'n'

        return github == 'y'

    def __input_user(self) -> str:
        default_user: str = self.__exec_for_stdout(['git', 'config', '--global', 'user.name'])
        message: str = 'Github pseudo'
        message += ' (' + default_user + ') :' if len(default_user) else ' : '
        user: str = input(message)
        user = user if user else default_user
        return user

    def __input_token(self) -> str:
        if self.config_handler.has_issuer() and self.config_handler.config.github.token is not None:
            keep_token: str = input('You already have a token, do you want to keep it? (y)/n : ')
            keep_token = keep_token if keep_token else 'y'
            if keep_token == 'y':
                return self.config_handler.config.github.token
        token: str = input('Token api Github : ')
        return token

    def __check_user(self):
        r: Response = Github(self.config_handler).get_user()
        if r.status_code != 200:
            raise ConnectionAbortedError('Bad api github token : retry')

    def add_to_config_handler(self) -> ConfigGithub:
        activate: bool = self.__input_github()
        github: ConfigGithub
        if activate:
            user: str = self.__input_user()
            token: str = self.__input_token()
            github = ConfigGithub(activate=activate, user=user, token=token)
            self.config_handler.config = self.config_handler.config.with_github(github)
            self.__check_user()
        else:
            user_opt: Optional[str] = None
            token_opt: Optional[str] = None
            github = ConfigGithub(activate=activate, user=user_opt, token=token_opt)
            self.config_handler.config = self.config_handler.config.with_github(github)
        return github
