from __future__ import annotations

from pprint import pprint

from Branches.Actions.Topicer.TopicBuilder import TopicBuilder
from Core.ConfigHandler import ConfigHandler
from FlexioFlow.Actions.TopicActions import TopicActions
from FlexioFlow.StateHandler import StateHandler
from typing import Dict, Optional, List

from Log.Log import Log
from VersionControl.VersionControl import VersionControl
from VersionControlProvider.Flexio.Topic.CommonTopic import CommonTopic
from VersionControlProvider.Topic import Topic as AbstractTopic


class Topic:

    def __init__(self,
                 action: TopicActions,
                 state_handler: StateHandler,
                 version_control: VersionControl,
                 config_handler: ConfigHandler,
                 options: Dict[str, str],
                 ) -> None:
        self.action: TopicActions = action
        self.state_handler: StateHandler = state_handler
        self.version_control: VersionControl = version_control
        self.config_handler: ConfigHandler = config_handler
        self.options: Dict[str, str] = options

    def process(self):

        if self.action is TopicActions.READ:
            topic_builder: TopicBuilder = TopicBuilder(
                self.version_control,
                self.state_handler,
                self.config_handler,
                None,
                self.options
            )

            topics: Optional[List[AbstractTopic]] = topic_builder.find_topic_from_branch_name().topics()

            if topics is not None and len(topics) > 0:
                for topic in topics:
                    Log.info('waiting... from flexio...')

                    read_topic: Optional[AbstractTopic] = topic_builder.topicer().read_topic_by_number(
                        int(topic.number))
                    if read_topic is not None:
                        CommonTopic.print_resume_topic(read_topic)
            else:
                Log.warning('No Topic found')
