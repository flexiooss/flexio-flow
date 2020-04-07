from __future__ import annotations

from typing import Optional, Dict, List

from Branches.Branches import Branches
from Core.ConfigHandler import ConfigHandler
from Core.TopicerHandler import TopicerHandler
from FlexioFlow.StateHandler import StateHandler
from Log.Log import Log
from VersionControl.VersionControl import VersionControl
from VersionControlProvider.Flexio.Topic.CommonTopic import CommonTopic
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic
from VersionControlProvider.Topicer import Topicer
from ConsoleColors.Fg import Fg


class TopicBuilder:
    def __init__(self,
                 version_control: VersionControl,
                 state_handler: StateHandler,
                 config_handler: ConfigHandler,
                 branch: Optional[Branches],
                 options: Dict[str, str]
                 ):
        self.__version_control: VersionControl = version_control
        self.__state_handler: StateHandler = state_handler
        self.__config_handler: ConfigHandler = config_handler
        self.__branch: Optional[Branches] = branch
        self.__topicer: Optional[Topicer] = None
        self.__topics: Optional[List[Topic]] = None
        self.__options: Dict[str, str] = options
        self.__init_topicer()

    def __init_topicer(self):
        if self.__config_handler.has_topicer():
            self.__topicer: Optional[Topicer] = TopicerHandler(
                self.__state_handler,
                self.__config_handler
            ).topicer()

    def __build_default(self):
        self.__topics = []
        for defaultTopic in self.__state_handler.default_topics():
            self.__topics.append(self.__topicer.from_default(defaultTopic))

    def try_ensure_topic(self) -> TopicBuilder:

        if self.__config_handler.has_topicer() and self.__topicer is not None:
            if self.__state_handler.has_default_topic():

                Log.info('waiting for... default Topics...')
                self.__build_default()
                Log.info(str(len(self.__topics)) + ' Topics found')

                if self.__topics is not None:
                    for topic in self.__topics:
                        CommonTopic.print_resume_topic(topic)

                    if self.__options.get('default') is None:

                        use_default_topic: str = input(
                            'Use these topics ' + Fg.SUCCESS.value + 'y' + Fg.RESET.value + '/n : ')
                        if use_default_topic.lower() == 'n':
                            self.__topics = None
            else:
                Log.info('No default Topic found')

            if self.__topics is None and self.__options.get('default') is None:
                self.__topics: List[Topic] = self.__topicer.attach_or_create()

        return self

    def attach_issue(self, issue: Issue) -> TopicBuilder:
        if self.__topics is not None:
            for topic in self.__topics:
                Log.info('Waiting... Attach issue to topics : ' + str(topic.number))
                self.__topicer.attach_issue(topic, issue)
        return self

    def find_topic_from_branch_name(self) -> TopicBuilder:
        if self.__topicer is not None:
            topics_number: Optional[List[int]] = self.__version_control.get_topics_number()
            if topics_number is not None and len(topics_number) > 0:
                self.__topics = []
                for number in topics_number:
                    self.__topics.append(self.__topicer.topic_builder().with_number(number))

            if self.__topics is not None and len(self.__topics) > 0:
                for topic in self.__topics:
                    Log.info('Topic number ' + str(topic.number) + ' found')
            else:
                Log.info('No Topic found')

        return self

    def topics(self) -> Optional[List[Topic]]:
        return self.__topics

    def topicer(self) -> Optional[Topicer]:
        return self.__topicer
