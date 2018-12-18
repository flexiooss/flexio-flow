from __future__ import annotations

from Core.Actions.Actions import Actions
from Core.Actions.Config import Config
from pathlib import Path

from Core.ConfigHandler import ConfigHandler


class Core:
    CONFIG_DIR: Path = Path.home().joinpath('.flexio-flow')

    def __init__(self, action: Actions):
        self.action: Actions = action
        self.config_handler = ConfigHandler(self.CONFIG_DIR)

    def process(self):
        if self.action is Actions.CONFIG:
            self.config()
        else:
            raise ValueError("Bad Core Action : " + self.action.value)

    def config(self):
        Config(self).process()

    def file_exists(self) -> bool:
        return self.CONFIG_FILE.is_file()
