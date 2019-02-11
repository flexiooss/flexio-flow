from __future__ import annotations
from typing import List, Dict, Type
from requests import Response
from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Flexio.FlexioIssue import FlexioIssue
from VersionControlProvider.Flexio.FlexioRequestApiError import FlexioRequestApiError
from VersionControlProvider.Flexio.FlexioTopic import FlexioTopic
from VersionControlProvider.Github.GithubRequestApiError import GithubRequestApiError
from VersionControlProvider.Github.Ressources.IssueGithub import IssueGithub
from VersionControlProvider.Github.Ressources.Milestone import Milestone
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic
# TODO finish class

class Create:
    topic: FlexioTopic

    def __init__(self, config_handler: ConfigHandler):
        self.__config_handler: ConfigHandler = config_handler

    def with_topic(self, topic: FlexioTopic) -> Create:
        self.topic = topic
        return self

    def __would_attach_topic(self) -> bool:
        topic: str = input('Have already a topic y/(n) : ')
        topic = topic if topic else 'n'
        return topic == 'y'

    def __number_topic(self) -> int:
        topic: str = input('Topic number : ')
        return int(topic)

    def __start_message(self) -> Create:
        print(
            """###############################################
################# Flexio FLow #################
###############################################
""")
        return self

    def __start_message_topic(self) -> Create:
        print(
            """###############################################
#############    Create Flexio Topic     #############
""")
        return self

    def __sanitize_list_input(self, v: List[str]) -> List[str]:
        return list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), v)))

    def __input_assignees(self, issue: IssueGithub) -> Create:
        message: str = '[separator `;`] Assignees'
        message += ' (' + self.__config_handler.config.github.user + ') :' if len(
            self.__config_handler.config.github.user) else ''
        message += ' < pseudo | `-l` to list users > : '

        assignees: str = input(message)
        assignees = assignees if assignees else self.__config_handler.config.github.user
        if assignees == '-l':
            r: Response = self.__github.get_users()
            members: List[str] = []
            if r.status_code is 200:
                members_response: List[Dict[str, str]] = r.json()
                l: Dict[str, str]
                for l in members_response:
                    members.append('{login!s}'.format(
                        login=l.get('login')
                    ))
            if len(members):
                message: str = """{0!s} 

Choose pseudo :
""".format(' | '.join(members))
            else:
                message: str = 'No member, type `abort`'
            assignees: str = input(message)

        assignees: List[str] = assignees.split(';')
        assignees = self.__sanitize_list_input(assignees)

        if len(assignees):
            issue.assignees = assignees
        return self

    def __create_milestone(self) -> Milestone:
        milestone: Milestone = Milestone()
        title: str = ''

        while not len(title) > 0:
            title = input('[required] Title : ')
            milestone.title = title

        description: str = input('Description : ')
        if description:
            milestone.description = description

        return milestone

    def __resume_milestone(self, milestone: Dict[str, str]) -> Create:
        print(
            """###############################################
################ Milestone created ################
###############################################
title : {title!s}
number : {number!s}
url : {url!s}
###############################################
""".format(
                title=milestone.get('title'),
                number=milestone.get('number'),
                url=milestone.get('html_url')
            )
        )
        return self

    def __input_milestone(self, issue: IssueGithub) -> Create:
        milestone: str = input(
            'Milestone number < number | `-l` to list the existing | `-c` to create milestone > ')
        if milestone == '-c':
            r1: Response = self.__github.get_open_milestones()
            milestones_repo: List[str] = []
            if r1.status_code is 200:
                milestones_response: List[Dict[str, str]] = r1.json()
                l: Dict[str, str]
                for l in milestones_response:
                    milestones_repo.append('{number!s} : {title!s}'.format(
                        number=l.get('number'),
                        title=l.get('title')
                    ))

            if len(milestones_repo):
                message: str = """{0!s}

Choose number : 
""".format(' | '.join(milestones_repo))
            else:
                message: str = 'No milestone, type `-c` to create milestone or `-a` for abort'

            milestone: str = input(message)

        if milestone == '-c':
            milestone_inst: Milestone = self.__create_milestone()
            r2: Response = self.__github.create_milestone(milestone_inst)
            if r2.status_code is 201:
                milestone_created: Dict[str, str] = r2.json()
                milestone = milestone_created.get('number')
                self.__resume_milestone(milestone_created)

        milestone = milestone if not milestone == '-a' else ''

        if milestone:
            issue.milestone = int(milestone)
        return self

    def __input_labels(self, issue: IssueGithub) -> Create:
        message: str = '[separator `;`] Labels : '
        r: Response = self.__github.get_labels()

        labels_repo: List[str] = []
        if r.status_code is 200:
            labels_response: List[Dict[str, str]] = r.json()
            l: Dict[str, str]
            for l in labels_response:
                labels_repo.append(l.get('name'))

        if len(labels_repo):
            message += """{0!s}

Choose label : 
""".format(' | '.join(labels_repo))

        labels: str = input(message)
        labels_lst: List[str] = labels.split(';')
        labels_lst = self.__sanitize_list_input(labels_lst)

        if len(labels_lst):
            issue.labels = labels_lst
        return self

    def __input_topic(self):
        issue: IssueGithub = IssueGithub()
        title: str = ''

        while not len(title) > 0:
            title = input('[required] Title : ')
        issue.title = title

        body: str = input('Description : ')
        if body:
            issue.body = body

        self.__input_assignees(issue).__input_milestone(issue).__input_labels(issue)

        return issue

    def __post_topic(self, issue: FlexioTopic) -> Response:
        return self.__github.create_issue(issue)

    def __resume_topic(self, topic: FlexioTopic) -> Create:
        print(
            """###############################################
################ Topic created ################
###############################################
title : {title!s}
number : {number!s}
url : {url!s}
###############################################
""".format(
                title=topic.title,
                number=topic.number,
                url=topic.url()
            )
        )
        return self

    def process(self) -> Topic:
        self.__start_message()


        topic_number: int
        if self.__would_attach_topic():
            topic_number = self.__number_topic()
            topic: FlexioTopic = FlexioTopic()

        else:
            self.__start_message_topic()

            topic: FlexioTopic = self.__input_topic()

            r: Response = self.__post_topic(topic)

            if r.status_code is 200:
                topic_created:FlexioTopic = FlexioTopic.build_from_api(r.json()[0])
                self.__resume_topic(topic_created)
            else:
                raise FlexioRequestApiError(r)

        return topic.with_number(topic_number)
