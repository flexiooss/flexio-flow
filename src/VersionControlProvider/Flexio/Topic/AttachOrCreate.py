from __future__ import annotations

from typing import List
from VersionControlProvider.Flexio.FlexioClient import Range

from requests import Response

from Core.ConfigHandler import ConfigHandler
from Log.Log import Log
from VersionControlProvider.Flexio.FlexioRequestApiError import FlexioRequestApiError
from VersionControlProvider.Flexio.FlexioTopic import FlexioTopic
from VersionControlProvider.Flexio.Topic.CommonTopic import CommonTopic
from VersionControlProvider.Flexio.Topic.Create import Create
from VersionControlProvider.Topic import Topic
from ConsoleColors.Fg import Fg


class AttachOrCreate:
    topic: FlexioTopic

    def __init__(self, config_handler: ConfigHandler):
        self.__config_handler: ConfigHandler = config_handler
        from VersionControlProvider.Flexio.FlexioClient import FlexioClient
        self.__flexio: FlexioClient = FlexioClient(self.__config_handler)
        self.__topics: List[Topic] = []

    def __would_attach_topics(self) -> bool:
        topic: str = input("""Have already topics {green}y{reset_fg}/n : """.format(
            green=Fg.SUCCESS.value,
            reset_fg=Fg.RESET.value,
        ))
        topic = topic if topic else 'y'
        return topic != 'n'

    def __list_topics(self, count: int):
        Log.info('waiting... Flexio... last 100 Topics')
        records: List[dict] = self.__get_last_100_records()
        for t_d in records:
            t: FlexioTopic
            t = FlexioTopic.build_from_api(t_d)
            print('{fg_cyan}{topic_number!s} : {topic_title!s}{reset_fg}'.format(
                fg_cyan=Fg.INFO.value,
                reset_fg=Fg.RESET.value,
                topic_number=t.number,
                topic_title=t.title
            ))
        return self.__topics_number()

    def __sanitize_list_input(self, v: List[str]) -> List[int]:
        return list(map(lambda x: int(x), filter(lambda x: len(x) > 0, map(lambda x: x.strip(), v))))

    def __topics_number(self) -> List[int]:
        topics_number: List[int] = []
        topics_number_input: str = input("""Topics number :
{bg_help}separator `;`{reset_bg}        
{bg_help}`-l` for list existing Topics{reset_bg} 
""".format(
            reset_bg=Fg.RESET.value,
            bg_help=Fg.INFO.value
        ))

        if topics_number_input == '-l':
            return self.__list_topics(100)
        else:
            topics: List[str] = topics_number_input.split(';')
            topics_number = self.__sanitize_list_input(topics)

        return topics_number

    def __get_last_100_records(self) -> List[dict]:
        topic: FlexioTopic = FlexioTopic()
        r: Range = self.__flexio.get_total(resource=topic)

        range: Range = Range()
        range.limit = r.total
        range.offset = 0 if r.total < r.accept_range else r.total - r.accept_range

        resp_records: Response = self.__flexio.get_records(topic, range)

        return resp_records.json()

    def __start_message(self) -> AttachOrCreate:
        print(
            """
###############################################
################ {yellow}FLEXIO TOPICER{reset} ###############
###############################################
""".format(yellow=Fg.FOCUS.value, reset=Fg.RESET.value))
        return self

    def __get_topic_with_number(self, topic: FlexioTopic) -> FlexioTopic:
        return FlexioTopic.build_from_api(self.__flexio.get_record(record=topic))

    def __create(self):
        Create(self.__config_handler).process()

    def __attach(self) -> bool:

        topic_number: int
        if self.__would_attach_topics():

            for topic_number in self.__topics_number():

                request_topic: FlexioTopic = FlexioTopic().with_number(topic_number)

                try:
                    Log.info('waiting... from Flexio... Topic : ' + str(topic_number))
                    topic: FlexioTopic = self.__get_topic_with_number(request_topic)
                    CommonTopic.print_resume_topic(topic)
                    self.__topics.append(topic)
                except FileNotFoundError:
                    Log.error(Fg.FAIL.value + 'Topic not found : retry' + Fg.RESET.value)
                    self.__topics = []
                    return self.process()
            return True
        else:
            return False

    def process(self) -> List[Topic]:
        self.__start_message()

        if self.__attach():
            return self.__topics
        else:
            self.__create()
            return self.process()
