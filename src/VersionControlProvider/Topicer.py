from __future__ import annotations
import abc
from typing import List

from Core.ConfigHandler import ConfigHandler
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.DefaultTopic import DefaultTopic
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic


class Topicer(abc.ABC):
    state_handler: StateHandler
    config_handler: ConfigHandler

    def __init__(self, state_handler: StateHandler, config_handler: ConfigHandler):
        self.state_handler: StateHandler = state_handler
        self.config_handler: ConfigHandler = config_handler

    @abc.abstractmethod
    def create(self) -> Topic:
        pass

    @abc.abstractmethod
    def attach_or_create(self) -> List[Topic]:
        pass

    @abc.abstractmethod
    def attach_issue(self, topic: Topic, issue: Issue) -> Topicer:
        pass

    @abc.abstractmethod
    def topic_builder(self) -> Topic:
        pass

    @abc.abstractmethod
    def from_default(self, topic: DefaultTopic) -> Topic:
        pass

    @abc.abstractmethod
    def read_topic_by_number(self, number: int) -> Topic:
        pass
