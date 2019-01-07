from __future__ import annotations
from typing import Dict, Union
from Core.Actions.Actions import Actions
from Core.Actions.Config import Config
from pathlib import Path

from Core.Actions.Read import Read
from Core.ConfigHandler import ConfigHandler
from Schemes.Schemes import Schemes


class Core:
    CONFIG_DIR: Path = Path.home().joinpath('.flexio-flow')

    def __init__(self, action: Actions, options: Dict[str, Union[str, Schemes, bool]], config_handler: ConfigHandler):
        self.action: Actions = action
        self.options: Dict[str, Union[str, Schemes, bool]] = options
        self.config_handler = config_handler

    def process(self):
        if self.action is Actions.CONFIG:
            if self.options.get('read', False):
                print('read config')
                self.read()
            else:
                self.config()
        else:
            raise ValueError("Bad Core Action : " + self.action.name)

    def config(self):
        Config(self.config_handler).process()

    def read(self):
        Read(self.config_handler).process()
