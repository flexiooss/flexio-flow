from __future__ import annotations
from typing import Dict, Union
from Core.Actions.Actions import Actions
from Core.Actions.Config import Config
from pathlib import Path
from Core.ConfigHandler import ConfigHandler
from Schemes.Schemes import Schemes


class Core:
    CONFIG_DIR: Path = Path.home().joinpath('.flexio-flow')

    def __init__(self, action: Actions, options: Dict[str, Union[str, Schemes]], config_handler: ConfigHandler):
        self.action: Actions = action
        self.options: Dict[str, Union[str, Schemes]] = options
        self.config_handler = config_handler

    def process(self):
        if self.action is Actions.CONFIG:
            self.config()
        else:
            raise ValueError("Bad Core Action : " + self.action.name)

    def config(self):
        Config(self.config_handler).process()
