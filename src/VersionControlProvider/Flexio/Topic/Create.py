from __future__ import annotations
from typing import List
from requests import Response
from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Flexio.FlexioClient import Range
from VersionControlProvider.Flexio.FlexioRequestApiError import FlexioRequestApiError
from VersionControlProvider.Flexio.FlexioTopic import FlexioTopic
from VersionControlProvider.Topic import Topic
from sty import fg, bg


class Create:
    topic: FlexioTopic

    def __init__(self, config_handler: ConfigHandler):
        self.__config_handler: ConfigHandler = config_handler
        from VersionControlProvider.Flexio.FlexioClient import FlexioClient
        self.__flexio: FlexioClient = FlexioClient(self.__config_handler)

    def with_topic(self, topic: FlexioTopic) -> Create:
        self.topic = topic
        return self

    def __would_attach_topic(self) -> bool:
        topic: str = input("""Have already a topic y/{green}n{reset_fg} : """.format(
            green=fg.green,
            reset_fg=fg.rs,
        ))
        topic = topic if topic else 'n'
        return topic == 'y'

    def __number_topic(self) -> int:
        topic: str = input("""Topic number :
         {bg_help}`-l` for list existing Topics{reset_bg}""".format(
            reset_bg=bg.rs,
            bg_help=bg.li_black
        ))

        if topic == '-l':
            records: List[dict] = self.__get_last_100_records()
            for t_d in records:
                t: FlexioTopic
                t = FlexioTopic.build_from_api(t_d)
                print('{topic_number!s} : {topic_title!s}'.format(
                    topic_number=t.number, topic_title=t.title))

                topic: str = input('Topic number : ')

        return int(topic)

    def __get_last_100_records(self) -> List[dict]:
        topic: FlexioTopic = FlexioTopic()
        r: Range = self.__flexio.get_total(resource=topic)

        range: Range = Range()
        range.limit = r.total
        range.offset = 0 if r.total < r.accept_range else r.total - r.accept_range

        resp_records: Response = self.__flexio.get_records(topic, range)

        return resp_records.json()

    def __get_topic_with_number(self, topic: FlexioTopic) -> FlexioTopic:
        return FlexioTopic.build_from_api(self.__flexio.get_record(record=topic))

    def __start_message(self) -> Create:
        print(
            """{fg_gray}###############################################
################# {yellow}Flexio FLow{fg_gray} #################
###############################################{reset}
""".format(yellow=fg.yellow, reset=fg.rs, fg_gray=fg(240)))
        return self

    def __start_message_topic(self) -> Create:
        print(
            """{fg_gray}###############################################
#############    {yellow}Create Flexio Topic{fg_gray}     #############{reset}
""".format(yellow=fg.yellow, reset=fg.rs, fg_gray=fg(240)))
        return self

    def __input_topic(self):
        issue: FlexioTopic = FlexioTopic()
        title: str = ''

        while not len(title) > 0:
            title = input(fg.red + '[required]' + fg.rs + ' Title : ')
        issue.title = title

        body: str = input('Description : ')
        if body:
            issue.body = body

        return issue

    def __post_topic(self, topic: FlexioTopic) -> Response:
        return self.__flexio.post_record(topic)

    def __resume_topic(self, topic: FlexioTopic) -> Create:
        print(
            """{fg_gray}###############################################
################ {green}Topic created{fg_gray} ################
###############################################{green}
title : {title!s}
number : {number!s}
url : {url!s}{fg_gray}
###############################################{reset}
""".format(
                green=fg.green,
                title=topic.title,
                number=topic.number,
                url=topic.url(),
                reset=fg.rs,
                fg_gray=fg(240)
            )
        )
        return self

    def process(self) -> Topic:
        self.__start_message()

        topic_number: int
        if self.__would_attach_topic():
            request_topic: FlexioTopic = FlexioTopic().with_number(self.__number_topic())

            try:
                topic: FlexioTopic = self.__get_topic_with_number(request_topic)
            except FileNotFoundError:
                print(fg.red + 'Topic not found : retry' + fg.rs)
                return self.process()

        else:
            self.__start_message_topic()

            topic: FlexioTopic = self.__input_topic()

            r: Response = self.__post_topic(topic)

            if r.status_code is 200:
                topic_created: FlexioTopic = FlexioTopic.build_from_api(r.json())
                self.__resume_topic(topic_created)
                topic = topic_created
            else:
                raise FlexioRequestApiError(r)

        return topic
