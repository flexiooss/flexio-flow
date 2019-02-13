import unittest
from pathlib import Path

from requests import Response

from Core.Config import Config
from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Flexio.ConfigFlexio import ConfigFlexio
from VersionControlProvider.Flexio.FlexioClient import FlexioClient, Range
from VersionControlProvider.Flexio.FlexioTopic import FlexioTopic
from VersionControlProvider.IssueState import IssueState
from tests.VersionControlProvider.Flexio.api___secret import USER_TOKEN
from sty import fg, bg

CONFIG_DIR: Path = Path('/tmp/')


class TestFlexio(unittest.TestCase):
    def setUp(self):
        self.config_handler = ConfigHandler(CONFIG_DIR)
        self.config_handler.config = Config().with_flexio(
            ConfigFlexio(
                activate=True,
                user_token=USER_TOKEN
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
            user_token='dudu'
        ))
        r: Response = FlexioClient(falsy_config_handler).post_record(record=topic)
        self.assertIsNot(r.status_code, 200)

    def test_get_last_record(self):
        topic: FlexioTopic = FlexioTopic()
        # topic.number = 2

        r: Response = FlexioClient(self.config_handler).get_records(record=topic, range=Range())

        print(r.headers)
        print(r.json())

        self.assertIn(r.status_code, [200, 206])

        expected_record_from_api: FlexioTopic = FlexioTopic.build_from_api(r.json()[0])

        r2: Response = FlexioClient(self.config_handler).get_records(record=expected_record_from_api, range=Range())

        record_from_api: FlexioTopic = FlexioTopic.build_from_api(r2.json()[0])

        self.assertDictEqual(record_from_api.to_api_dict(), expected_record_from_api.to_api_dict())

    def test_get_total(self):
        topic: FlexioTopic = FlexioTopic()
        r: Range = FlexioClient(self.config_handler).get_total(resource=topic)
        print('accept_range : ' + str(r.accept_range))
        print('offset : ' + str(r.offset))
        print('limit : ' + str(r.limit))
        print('total : ' + str(r.total))

    def test_get_last_100_records(self):
        topic: FlexioTopic = FlexioTopic()
        r: Range = FlexioClient(self.config_handler).get_total(resource=topic)

        range: Range = Range()
        range.limit = r.total
        range.offset = 0 if r.total < r.accept_range else r.total - r.accept_range

        resp_records: Response = FlexioClient(self.config_handler).get_records(topic, range)

        print(resp_records.headers)
        print(resp_records.json())

        for t_d in resp_records.json():
            t: FlexioTopic
            t = FlexioTopic.build_from_api(t_d)
            print('{topic_number!s} : {topic_title!s}'.format(
                topic_number=t.number, topic_title=t.title))

        self.assertIn(resp_records.status_code, [200, 206])

    def test_get_topic_by_number(self):
        topic: FlexioTopic = FlexioTopic().with_number(2)
        r: dict = FlexioClient(self.config_handler).get_record(record=topic)

        self.assertIsNotNone(r)
        record: FlexioTopic = FlexioTopic.build_from_api(r)
        self.assertEqual(topic.number, record.number)

        topic2: FlexioTopic = FlexioTopic().with_number(-5)
        with self.assertRaises(FileNotFoundError):
            FlexioClient(self.config_handler).get_record(record=topic2)

    def test_color(self):

        print(fg.red + 'bibi' + fg.rs)
        print('{color1!s} bibi {color_end!s}'.format(
            color1=bg.cyan, color_end=fg.rs))
        print('{color1!s} bibi {color_end!s}'.format(
            color1=bg.li_black, color_end=fg.rs))

        print(
            """{yellow}###############################################
################# Flexio FLow #################
###############################################{reset}
""".format(yellow=fg.yellow, reset=fg.rs))
