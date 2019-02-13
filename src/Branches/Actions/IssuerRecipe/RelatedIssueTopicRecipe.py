from __future__ import annotations

from typing import Optional

from Core.ConfigHandler import ConfigHandler
from Core.IssuerHandler import IssuerHandler
from Core.TopicerHandler import TopicerHandler
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Issuer import Issuer
from VersionControlProvider.Topic import Topic
from VersionControlProvider.Topicer import Topicer


class RelatedIssueTopicRecipe:
    def __init__(self,
                 state_handler: StateHandler,
                 config_handler: ConfigHandler
                 ):

        self.__state_handler: StateHandler = state_handler
        self.__config_handler: ConfigHandler = config_handler
        self.__issuer: Optional[Issuer] = IssuerHandler(
            self.__state_handler, self.__config_handler
        ).issuer()
        self.__issue: Optional[Issue] = None
        self.__topicer: Optional[Topicer] = None
        self.__topic: Optional[Topic] = None

        self.__init_topicer()

    def __init_topicer(self):
        if self.__config_handler.has_topicer():
            self.__topicer: Optional[Topicer] = TopicerHandler(
                self.__state_handler,
                self.__config_handler
            ).topicer()

    def __try_ensure_issue(self) -> RelatedIssueTopicRecipe:
        if self.__issuer is not None and self.__issuer.has_repo():
            self.__issue = self.__issuer.create()
        return self

    def __try_ensure_topic(self) -> RelatedIssueTopicRecipe:

        if self.__topicer is not None:
            self.__topic: Topic = self.__topicer.create()
        return self

    def __comment_issue_with_topic(self) -> RelatedIssueTopicRecipe:
        if self.__issue is not None and self.__topic is not None:
            self.__issuer.comment(self.__issue, self.__topic.url())
        return self

    def process(self) -> Optional[Issue]:
        self.__try_ensure_issue().__try_ensure_topic().__comment_issue_with_topic()
        return self.__issue
