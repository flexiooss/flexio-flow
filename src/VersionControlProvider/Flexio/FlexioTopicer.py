from __future__ import annotations

from VersionControlProvider.DefaultTopic import DefaultTopic
from VersionControlProvider.Flexio.FlexioClient import FlexioClient
from VersionControlProvider.Flexio.FlexioIssue import FlexioIssue
from VersionControlProvider.Flexio.Topic.Create import Create
from VersionControlProvider.Flexio.FlexioTopic import FlexioTopic
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic
from VersionControlProvider.Topicer import Topicer


class FlexioTopicer(Topicer):

    def create(self) -> Topic:
        return Create(config_handler=self.config_handler).process()

    def attach_issue(self, topic: Topic, issue: Issue) -> FlexioTopicer:
        flexio: FlexioClient = FlexioClient(self.config_handler)
        flexio.post_record(FlexioIssue().with_topic(topic).set_github_issue(issue))
        return self

    def topic_builder(self) -> Topic:
        return FlexioTopic()

    def from_default(self, default_topic: DefaultTopic) -> Topic:
        return FlexioTopic.build_from_api(
            FlexioClient(self.config_handler).get_record(FlexioTopic().with_number(default_topic.number)))

    def read_topic_by_number(self, number: int) -> Topic:
        return FlexioTopic.build_from_api(
            FlexioClient(self.config_handler).get_record(FlexioTopic().with_number(number)))
