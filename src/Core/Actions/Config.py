from __future__ import annotations

from subprocess import Popen, PIPE
from typing import List

from requests import Response

from Core.ConfigHandler import ConfigHandler
from Core.Config import Config as ConfigObjectValue
from VersionControlProvider.Github.Github import Github


class Config:
    def __init__(self, config_handler: ConfigHandler):
        self.config_handler: ConfigHandler = config_handler

    def __config_handler(self) -> ConfigHandler:
        return self.config_handler

    def __exec(self, args: List[str]):
        Popen(args, cwd=self.config_handler.dir_path.as_posix()).communicate()

    def __exec_for_stdout(self, args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE, cwd=self.config_handler.dir_path.as_posix()).communicate()
        return stdout.strip().decode('utf-8')

    def __start_message(self) -> Config:
        print(
            """###############################################
################# Flexio FLow Core #################
###############################################
#################    Config     #################
""")
        return self

    def __input_user(self) -> str:
        default_user: str = self.__exec_for_stdout(['git', 'config', 'user.email'])
        message: str = 'Github user'
        message += ' (' + default_user + ') :' if len(default_user) else ' : '
        user: str = input(message)
        user = user if user else default_user
        return user

    def __input_token(self) -> str:
        token: str = input('Token api Github : ')
        return token

    def __write_file(self) -> Config:
        yml: str = self.__config_handler().write_file()
        print("""#################################################
    Write file : {0!s} 
    #################################################""".format(self.__config_handler().file_path()))
        print(yml)
        return self

    def __final_message(self) -> Config:
        print(
            """###############################################
Enjoy with Flexio FLow 
###############################################
""")
        return self

    def __check_user(self, token: str):
        r: Response = Github(self.__config_handler().dir_path).with_token(token).get_user()
        if r.status_code is not 200:
            raise ConnectionAbortedError('Bad api github token : retry')

    def __ensure_have_config(self) -> Config:
        if self.__config_handler().file_exists():
            self.__config_handler().load_file_config()
            print(
                """###############################################
Flexio Flow  Core already initialized 
###############################################
""")
            print('at : ' + self.__config_handler().file_path().as_posix())
            print('with : ' + str(self.__config_handler().config.to_dict()))
            use: str = input('Use this file (y)/n : ')
            use = use if use else 'y'
            if use is 'y':
                return self

        if not self.config_handler.dir_path.exists():
            self.config_handler.dir_path.mkdir()

        self.__start_message()

        user: str = self.__input_user()
        token: str = self.__input_token()

        self.__check_user(token)
        self.__config_handler().config = ConfigObjectValue(user=user, token=token)
        self.__write_file()

        return self

    def process(self):
        self.__ensure_have_config()
        self.__final_message()
