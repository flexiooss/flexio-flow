from __future__ import annotations

from VersionControlProvider.Flexio.Topic.Create import Create
from VersionControlProvider.Flexio.FlexioTopic import FlexioTopic
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic
from VersionControlProvider.Topicer import Topicer


class FlexioTopicer(Topicer):

    def create(self) -> Topic:
        return Create(config_handler=self.config_handler).process()

    def create_with_issue(self, issue: Issue) -> Topic:
        return Create(config_handler=self.config_handler).with_issue(issue).process()

    def topic_builder(self) -> Topic:
        return FlexioTopic()
