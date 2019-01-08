import unittest
from pathlib import Path

from requests import Response

from Core.Config import Config
from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Flexio.ConfigFlexio import ConfigFlexio
from VersionControlProvider.Flexio.FlexioClient import FlexioClient
from VersionControlProvider.Flexio.FlexioTopic import FlexioTopic
from VersionControlProvider.IssueState import IssueState
from tests.VersionControlProvider.Flexio.api___secret import USER_TOKEN, SERVICE_TOKEN

CONFIG_DIR: Path = Path('/tmp/')


class TestFlexio(unittest.TestCase):
    def setUp(self):
        self.config_handler = ConfigHandler(CONFIG_DIR)
        self.config_handler.config = Config().with_flexio(ConfigFlexio(
            activate=True,
            user_token=USER_TOKEN,
            service_token=SERVICE_TOKEN
        ))

    def test_post_record(self):
        topic: FlexioTopic = FlexioTopic()
        topic.title = 'test'
        topic.body = 'dudu'
        topic.state = IssueState.OPEN

        print(topic.to_api_dict())

        r: Response = FlexioClient(self.config_handler).post_record(record=topic)


        topic_created: FlexioTopic = FlexioTopic.build_from_api(r.json())
        self.assertEqual(topic.title, topic_created.title)
        self.assertEqual(topic.body, topic_created.body)
        self.assertEqual(topic.state, topic_created.state)

        print(topic_created.__dict__())

        self.assertIs(r.status_code, 200)
        falsy_config_handler = ConfigHandler(CONFIG_DIR)
        falsy_config_handler.config = Config().with_flexio(ConfigFlexio(
            activate=True,
            user_token='dudu',
            service_token='dudu'
        ))
        r: Response = FlexioClient(falsy_config_handler).post_record(record=topic)
        self.assertIsNot(r.status_code, 200)
