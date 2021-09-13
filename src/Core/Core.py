from __future__ import annotations
from Core.Actions.Actions import Actions
from Core.Actions.Config import Config
from pathlib import Path

from Core.Actions.Read import Read
from Core.Actions.Branch import Branch
from Core.ConfigHandler import ConfigHandler
from FlexioFlow.Options import Options


class Core:
    CONFIG_DIR: Path = Path.home().joinpath('.flexio-flow')

    def __init__(self, action: Actions, options: Options, config_handler: ConfigHandler):
        self.action: Actions = action
        self.options: Options = options
        self.config_handler = config_handler

    def process(self):
        if self.action is Actions.CONFIG:
            if self.options.read:
                print('read config')
                self.read()
            else:
                self.config()
        elif self.action is Actions.BRANCH:
            self.branch()
        else:
            raise ValueError("Bad Core Action : " + self.action.name)

    def config(self):
        Config(self.config_handler).process()

    def read(self):
        Read(self.config_handler).process()

    def branch(self):
        raise FileNotFoundError('not implemented yet')
        Branch(self.config_handler).process()
