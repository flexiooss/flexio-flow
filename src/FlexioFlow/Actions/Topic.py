from __future__ import annotations

from pprint import pprint

from Branches.Actions.Topicer.TopicBuilder import TopicBuilder
from Core.ConfigHandler import ConfigHandler
from FlexioFlow.Actions.IssueActions import IssueActions
from FlexioFlow.Actions.TopicActions import TopicActions
from FlexioFlow.StateHandler import StateHandler
from typing import Dict, Optional

from Log.Log import Log
from VersionControl.VersionControl import VersionControl
from VersionControlProvider.Topic import Topic as AbstractTopic


class Topic:

    def __init__(self,
                 action: IssueActions,
                 state_handler: StateHandler,
                 version_control: VersionControl,
                 config_handler: ConfigHandler,
                 options: Dict[str, str],
                 ) -> None:
        self.action: IssueActions = action
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

            topic: Optional[AbstractTopic] = topic_builder.find_topic_from_branch_name().topic()

            if topic is not None:
                Log.info('waiting... from flexio...')

                read_topic: Optional[AbstractTopic] = topic_builder.topicer().read_topic_by_number(int(topic.number))
                if read_topic is not None:
                    pprint(read_topic.to_dict())
