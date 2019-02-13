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
from sty import fg, bg


class Create:
    def __init__(self, config_handler: ConfigHandler, repo: Repo):
        self.__config_handler: ConfigHandler = config_handler
        self.__repo = repo
        self.__github = Github(self.__config_handler).with_repo(self.__repo)

    def __would_attach_issue(self) -> bool:
        issue: str = input("""Have already an issue y/{green}n{reset_fg} : """.format(
            green=fg.green,
            reset_fg=fg.rs,
        ))
        issue = issue if issue else 'n'
        return issue == 'y'

    def __number_issue(self) -> int:
        issue: str = input('Issue number : ')
        return int(issue)

    def __start_message(self) -> Create:
        print(
            """{fg_gray}###############################################
################# {yellow}Flexio FLow{fg_gray} #################
###############################################{reset}
""".format(fg_gray=fg(240), yellow=fg.yellow, reset=fg.rs))
        return self

    def __start_message_issue(self) -> Create:
        print(
            """{fg_gray}###############################################
##########     {yellow}Create Github Issue{fg_gray}     ##########{reset}
""".format(fg_gray=fg(240), yellow=fg.yellow, reset=fg.rs))
        return self

    def __sanitize_list_input(self, v: List[str]) -> List[str]:
        return list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), v)))

    def __input_assignees(self, issue: IssueGithub) -> Create:
        message: str = """ Assignees {default}
{bg_help}separator `;`{reset_bg}
{bg_help}`-l` to list users{reset_bg}
""".format(
            default=fg.green + self.__config_handler.config.github.user + fg.rs + ' :' if len(
                self.__config_handler.config.github.user) else '',
            reset_bg=bg.rs,
            bg_help=bg.li_black
        )

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
                message: str = """{fg_cyan}{members!s} {reset_fg}

Choose pseudo :
""".format(fg_cyan=fg.cyan,
           members=' | '.join(members),
           reset_fg=fg.rs
           )
            else:
                message: str = fg.red + 'No member, type `abort`' + fg.rs
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
            title = input(fg.red + '[required]' + fg.rs + ' Title : ')
            milestone.title = title

        description: str = input('Description : ')
        if description:
            milestone.description = description

        return milestone

    def __resume_milestone(self, milestone: Dict[str, str]) -> Create:
        print(
            """{fg_gray}###############################################
################ {green}Milestone created{fg_gray} ################
###############################################{green}
title : {title!s}
number : {number!s}
url : {url!s}
{fg_gray}###############################################{reset}
""".format(
                green=fg.green,
                title=milestone.get('title'),
                number=milestone.get('number'),
                url=milestone.get('html_url'),
                reset=fg.rs,
                fg_gray=fg(240)
            )
        )
        return self

    def __input_milestone(self, issue: IssueGithub) -> Create:

        milestone: str = input(
            """Milestone number : 
{bg_help}`-l` to list the existing 
`-c` to create milestone{reset_bg}""".format(
                reset_bg=bg.rs,
                bg_help=bg.li_black
            ))

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
                message: str = """{fg_cyan}{milestones!s}{fg_reset}

Choose number : 
""".format(
                    fg_cyan=fg.cyan,
                    milestones=' | '.join(milestones_repo),
                    fg_reset=fg.rs
                )
            else:
                message: str = fg.red + 'No milestone, type `-c` to create milestone or `-a` for abort' + fg.rs

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
        message: str = 'Labels '
        r: Response = self.__github.get_labels()

        labels_repo: List[str] = []
        if r.status_code is 200:
            labels_response: List[Dict[str, str]] = r.json()
            l: Dict[str, str]
            for l in labels_response:
                labels_repo.append(l.get('name'))

        if len(labels_repo):
            message += """{fg_cyan}{labels!s}{fg_reset}

Choose label : 
{bg_help}separator `;` {reset_bg}
""".format(
                fg_cyan=fg.cyan,
                labels=' | '.join(labels_repo),
                fg_reset=fg.rs,
                reset_bg=bg.rs,
                bg_help=bg.li_black
            )

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
            title = input(fg.red + '[required]' + fg.rs + ' Title : ')
        issue.title = title

        body: str = input('Description : ')
        if body:
            issue.body = body

        self.__input_assignees(issue).__input_labels(issue)

        return issue

    def __post_issue(self, issue: IssueGithub) -> Response:
        return self.__github.create_issue(issue)

    def __resume_issue(self, issue: IssueGithub) -> Create:
        print(
            """{fg_gray}###############################################
################ {green}Issue created {fg_gray}################
###############################################{green}
title : {title!s}
number : {number!s}
url : {url!s}{fg_gray}
###############################################{reset}
""".format(
                green=fg.green,
                title=issue.title,
                number=issue.number,
                url=issue.url,
                reset=fg.rs,
                fg_gray=fg(240)
            )
        )

        return self

    def process(self) -> Issue:
        self.__start_message()
        issue_number: int
        issue_url: str
        if self.__would_attach_issue():
            issue_number = self.__number_issue()
            issue: IssueGithub = IssueGithub().with_number(issue_number)

        else:
            self.__start_message_issue()

            issue: IssueGithub = self.__input_issue()

            r: Response = self.__post_issue(issue)

            if r.status_code is 201:
                issue_created: IssueGithub = IssueGithub.from_api_dict(r.json())

                self.__resume_issue(issue_created)
                issue = issue_created
            else:
                raise GithubRequestApiError(r)

        return issue
