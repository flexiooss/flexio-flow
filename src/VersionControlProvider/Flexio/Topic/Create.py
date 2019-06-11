from __future__ import annotations
from typing import List
from requests import Response
from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Flexio.FlexioRequestApiError import FlexioRequestApiError
from VersionControlProvider.Flexio.FlexioTopic import FlexioTopic
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic
from sty import fg, bg


class Create:
    topic: FlexioTopic

    def __init__(self, config_handler: ConfigHandler):
        self.__config_handler: ConfigHandler = config_handler
        from VersionControlProvider.Flexio.FlexioClient import FlexioClient
        self.__flexio: FlexioClient = FlexioClient(self.__config_handler)



    def __get_topic_with_number(self, topic: FlexioTopic) -> FlexioTopic:
        return FlexioTopic.build_from_api(self.__flexio.get_record(record=topic))

    def __start_message(self) -> Create:
        print(
            """{fg_gray}###############################################
#################### {yellow}TOPIC{fg_gray} ####################
###############################################{reset}
""".format(yellow=fg.yellow, reset=fg.rs, fg_gray=fg(240)))
        return self

    def __start_message_topic(self) -> Create:
        print(
            """{fg_gray}###############################################
#########    {yellow}Create Flexio Topic{fg_gray}     ##########{reset}
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

        self.__start_message_topic()

        topic: FlexioTopic = self.__input_topic()

        r: Response = self.__post_topic(topic)

        if r.status_code is 200:
            topic_created: FlexioTopic = FlexioTopic.build_from_api(r.json())
            print(topic_created.to_api_dict())
            self.__resume_topic(topic_created)
            topic = topic_created
        else:
            raise FlexioRequestApiError(r)

        return topic
