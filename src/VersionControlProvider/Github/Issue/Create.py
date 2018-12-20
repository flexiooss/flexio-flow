from __future__ import annotations

from typing import List, Dict, Type

from requests import Response

from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Github.Github import Github
from VersionControlProvider.Github.GithubRequestApiError import GithubRequestApiError
from VersionControlProvider.Github.IssueGithub import IssueGithub
from VersionControlProvider.Github.Repo import Repo
from VersionControlProvider.Issue import Issue


class Create:
    def __init__(self, config_handler: ConfigHandler, repo: Repo):
        self.__config_handler: ConfigHandler = config_handler
        self.__repo = repo
        self.__github = Github(self.__config_handler).with_repo(self.__repo)

    def __would_attach_issue(self) -> bool:
        issue: str = input('Have already an issue y/(n) : ')
        issue = issue if issue else 'n'
        return issue == 'y'

    def __number_issue(self) -> int:
        issue: str = input('Issue number : ')
        return int(issue)

    def __start_message(self) -> Create:
        print(
            """###############################################
################# Flexio FLow #################
###############################################
#############    Create Issue     #############
""")
        return self

    def __input_issue(self):
        issue: IssueGithub = IssueGithub()
        title: str = ''

        while not len(title) > 0:
            title = input('[required] Title : ')
        issue.title = title

        body: str = input('Description : ')
        if body:
            issue.body = body

        message: str = '[separator `;`] Assignees'
        message += ' (' + self.__config_handler.config.github.user + ') :' if len(
            self.__config_handler.config.github.user) else ' : '

        assignees: str = input(message)
        assignees = assignees if assignees else self.__config_handler.config.github.user
        assignees: List[str] = assignees.split(';')
        assignees = list(map(lambda x: x.strip(), assignees))

        if len(assignees):
            issue.assignees = assignees

        milestone: str = input('Milestone number : ')
        if milestone:
            issue.milestone = int(milestone)

        message: str = '[separator `;`] Labels : '
        r: Response = self.__github.get_labels()

        labels_repo: List[str] = []
        if r.status_code is 200:
            labels_response: List[Dict[str, str]] = r.json()
            l: Dict[str, str]
            for l in labels_response:
                labels_repo.append(l.get('name'))

        if len(labels_repo):
            message += """ 
Choose between : {0!s}
""".format(' | '.join(labels_repo))

        labels: str = input(message)
        labels: List[str] = labels.split(';')
        labels = list(map(lambda x: x.strip(), labels))

        if len(labels):
            issue.labels = labels

        return issue

    def __post_issue(self, issue: IssueGithub) -> Response:
        return self.__github.create_issue(issue)

    def __resume_issue(self, issue: Dict[str, str]) -> Create:
        print(
            """###############################################
################ Issue created ################
###############################################
title : {title!s}
number : {number!s}
url : {url!s}
###############################################
""".format(
                title=issue.get('title'),
                number=issue.get('number'),
                url=issue.get('url')
            )
        )
        return self

    def process(self) -> IssueGithub:
        issue_number: int
        if self.__would_attach_issue():
            issue_number = self.__number_issue()
            issue: IssueGithub = IssueGithub()

        else:
            self.__start_message()

            issue: IssueGithub = self.__input_issue()

            r: Response = self.__post_issue(issue)

            if r.status_code is 201:
                issue_created: Dict[str, str] = r.json()
                issue_number = issue_created.get('number')
                self.__resume_issue(issue_created)
            else:
                raise GithubRequestApiError(r)

        print(issue_number)
        return issue.with_number(issue_number)
