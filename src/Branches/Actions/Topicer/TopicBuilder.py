from __future__ import annotations

from typing import Optional, Dict

from Branches.Branches import Branches
from Core.ConfigHandler import ConfigHandler
from Core.TopicerHandler import TopicerHandler
from FlexioFlow.StateHandler import StateHandler
from Log.Log import Log
from VersionControl.VersionControl import VersionControl
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
        self.__topic: Optional[Topic] = None
        self.options: Dict[str, str] = options
        self.__init_topicer()

    def __init_topicer(self):
        if self.__config_handler.has_topicer():
            self.__topicer: Optional[Topicer] = TopicerHandler(
                self.__state_handler,
                self.__config_handler
            ).topicer()

    def __build_default(self):
        self.__topic = self.__topicer.from_default(self.__state_handler.default_topic())

    def try_ensure_topic(self) -> TopicBuilder:

        if self.__config_handler.has_topicer() and self.__topicer is not None:
            if self.__state_handler.has_default_topic():
                Log.info('waiting... default Topic...')
                self.__build_default()

                print(
                    """
###############################################
############{green}    Default Topic     {reset}############
###############################################{green}
title : {title!s}
number : {number!s}
description : {body!s}
url : {url!s}{reset}
###############################################
""".format(
                        green=Fg.FOCUS.value,
                        title=self.__topic.title,
                        number=self.__topic.number,
                        body=self.__topic.body,
                        url=self.__topic.url(),
                        reset=Fg.RESET.value
                    )
                )

            use_default_topic: str = input('Use this topic Y/N : ' + Fg.SUCCESS.value + 'Y' + Fg.RESET.value)
            if use_default_topic.lower() == 'n':
                self.__topic = None

            if self.__topic is None:
                self.__topic: Topic = self.__topicer.create()

        return self

    def attach_issue(self, issue: Issue) -> TopicBuilder:
        if self.__topic is not None:
            Log.info('Waiting... Attach issue to topic...')
            self.__topicer.attach_issue(self.__topic, issue)
        return self

    def find_topic_from_branch_name(self) -> TopicBuilder:
        if self.__topicer is not None:
            topic_number: Optional[int] = self.__version_control.get_topic_number()
            if topic_number is not None:
                self.__topic = self.__topicer.topic_builder().with_number(topic_number)
                if self.__topic is not None:
                    Log.info('Topic number ' + str(self.__topic.number) + ' found')
            else:
                Log.info('No Topic found')

        return self

    def topic(self) -> Optional[Issue]:
        return self.__topic

    def topicer(self) -> Optional[Topicer]:
        return self.__topicer
