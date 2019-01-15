from subprocess import Popen, PIPE
from typing import Optional, List

# from requests import Response

from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Flexio.ConfigFlexio import ConfigFlexio


# from VersionControlProvider.Flexio.FlexioClient import FlexioClient


class InputConfig:
    def __init__(self, config_handler: ConfigHandler):
        self.config_handler: ConfigHandler = config_handler

    def __exec_for_stdout(self, args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE, cwd=self.config_handler.dir_path.as_posix()).communicate()
        return stdout.strip().decode('utf-8')

    def __input_flexio(self) -> bool:
        flexio: str = input('Activate Flexio automatic topicer (y)/n :')
        flexio = flexio if flexio else 'y'
        return flexio == 'y'

    def __input_user_token(self) -> str:
        token: str = input('User token api Flexio : ')
        return token

    # def __check_user(self):
    #     r: Response = FlexioClient(self.config_handler).get_user()
    #     if r.status_code is not 200:
    #         raise ConnectionAbortedError('Bad api flexio token : retry')

    def add_to_config_handler(self) -> ConfigFlexio:
        activate: bool = self.__input_flexio()
        flexio: ConfigFlexio
        if activate:
            user: str = self.__input_user_token()
            flexio = ConfigFlexio(activate=activate, user_token=user)
            self.config_handler.config = self.config_handler.config.with_flexio(flexio)
            # self.__check_user()
        else:
            user_opt: Optional[str] = None
            flexio = ConfigFlexio(activate=activate, user_token=user_opt)
            self.config_handler.config = self.config_handler.config.with_flexio(flexio)
        return flexio
