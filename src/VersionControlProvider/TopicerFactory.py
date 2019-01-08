from __future__ import annotations

from Core.ConfigHandler import ConfigHandler
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.Flexio.FlexioTopicer import FlexioTopicer
from VersionControlProvider.Topicer import Topicer
from VersionControlProvider.Topicers import Topicers


class TopicerFactory:

    @staticmethod
    def build(
            state_handler: StateHandler,
            config_handler: ConfigHandler,
            topicer: Topicers
    ) -> Topicer:
        if topicer is Topicers.FLEXIO:
            return FlexioTopicer(state_handler, config_handler)

        raise NotImplementedError
