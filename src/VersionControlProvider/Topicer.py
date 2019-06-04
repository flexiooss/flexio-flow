from __future__ import annotations
import abc

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
    def create_with_issue(self, issue: Issue) -> Topic:
        pass

    @abc.abstractmethod
    def topic_builder(self) -> Topic:
        pass

    @abc.abstractmethod
    def from_default(self, topic: DefaultTopic) -> Topic:
        pass
