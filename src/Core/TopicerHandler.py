from typing import Optional

from Core.ConfigHandler import ConfigHandler
from FlexioFlow.StateHandler import StateHandler

from VersionControlProvider.Topicer import Topicer
from VersionControlProvider.TopicerBuilder import TopicerBuilder
from VersionControlProvider.Topicers import Topicers


class TopicerHandler:
    def __init__(self, state_handler: StateHandler, config_handler: ConfigHandler):
        self.state_handler: StateHandler = state_handler
        self.config_handler: ConfigHandler = config_handler

    def topicer(self) -> Optional[Topicer]:
        topicers: Topicers = Topicers.FLEXIO
        topicer: Topicer = TopicerBuilder.build(self.state_handler, self.config_handler, topicers)
        return topicer
