from __future__ import annotations
from typing import List, Dict, Type
from requests import Response
from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Github.Github import Github
from VersionControlProvider.Github.GithubRequestApiError import GithubRequestApiError
from VersionControlProvider.Github.Ressources.IssueGithub import IssueGithub
from VersionControlProvider.Github.Repo import Repo
from VersionControlProvider.Github.Ressources.Milestone import Milestone
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
""")
        return self

    def __start_message_issue(self) -> Create:
        print(
            """###############################################
#############    Create Issue     #############
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

    def __input_issue(self):
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
                url=issue.get('html_url')
            )
        )
        return self

    def process(self) -> Issue:
        self.__start_message()
        issue_number: int
        issue_url: str
        if self.__would_attach_issue():
            issue_number = self.__number_issue()
            issue: IssueGithub = IssueGithub()

        else:
            self.__start_message_issue()

            issue: IssueGithub = self.__input_issue()

            r: Response = self.__post_issue(issue)

            if r.status_code is 201:
                issue_created: Dict[str, str] = r.json()
                issue_number = issue_created.get('number')
                issue_url = issue_created.get('url')
                self.__resume_issue(issue_created)
            else:
                raise GithubRequestApiError(r)

        return issue.with_number(issue_number).with_url(issue_url)
