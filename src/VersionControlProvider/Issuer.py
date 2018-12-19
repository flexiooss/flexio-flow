from __future__ import annotations
import abc
from typing import Type

from Core.ConfigHandler import ConfigHandler


class Issuer(abc.ABC):

    def __init__(self, config_handler: ConfigHandler):
        self.config_handler: ConfigHandler = config_handler

    @abc.abstractmethod
    def process(self) -> str:
        pass
