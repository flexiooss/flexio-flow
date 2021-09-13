from __future__ import annotations

from Core.ConfigHandler import ConfigHandler


class Branch:
    def __init__(self, config_handler: ConfigHandler):
        self.config_handler: ConfigHandler = config_handler

    def __config_handler(self) -> ConfigHandler:
        return self.config_handler

    def process(self):
        return
