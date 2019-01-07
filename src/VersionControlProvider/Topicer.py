from __future__ import annotations
import abc

from Core.ConfigHandler import ConfigHandler
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.Topic import Topic


class Topicer(abc.ABC):
    state_handler: StateHandler
    config_handler: ConfigHandler

    def __init__(self, state_handler: StateHandler, config_handler: ConfigHandler):
        self.state_handler: StateHandler = state_handler
        self.config_handler: ConfigHandler = config_handler
        self.__repo = None

    @abc.abstractmethod
    def create(self) -> Topic:
        pass

    @abc.abstractmethod
    def topic_builder(self) -> Topic:
        pass
