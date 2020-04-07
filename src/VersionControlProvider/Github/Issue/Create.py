from __future__ import annotations
from typing import List, Dict, Type, Optional
from requests import Response
from Core.ConfigHandler import ConfigHandler
from Log.Log import Log
from VersionControlProvider.Github.Github import Github
from VersionControlProvider.Github.GithubRequestApiError import GithubRequestApiError
from VersionControlProvider.Github.Issue.CommonIssue import CommonIssue
from VersionControlProvider.Github.Ressources.IssueGithub import IssueGithub
from VersionControlProvider.Github.Repo import Repo
from VersionControlProvider.Github.Ressources.Milestone import Milestone
from VersionControlProvider.Issue import Issue
from ConsoleColors.Fg import Fg

from VersionControlProvider.IssueDefault import IssueDefault


class Create:
    def __init__(self, config_handler: ConfigHandler, repo: Repo, default_issue: Optional[IssueDefault],
                 options: Optional[Dict[str, str]]):
        self.__config_handler: ConfigHandler = config_handler
        self.__repo: Repo = repo
        self.__github = Github(self.__config_handler).with_repo(self.__repo)
        self.__default_issue: Optional[IssueDefault] = default_issue
        self.__options: Optional[Dict[str, str]] = options

    def __start_message(self) -> Create:
        if self.__options.get('default') is None:
            CommonIssue.issuer_message()
        return self

    def __start_message_issue(self) -> Create:
        if self.__options.get('default') is None:
            print(
            """###############################################
#########     {yellow}Create Github Issue{reset}     #########
""".format(yellow=Fg.NOTICE.value, reset=Fg.RESET.value))
        return self

    def __sanitize_list_input(self, v: List[str]) -> List[str]:
        return list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), v)))

    def __input_assignees(self, issue: IssueGithub) -> Create:
        if self.__options.get('default') is not None:
            assignees: List[str] = self.__default_issue.assignees
        else:
            message: str = """ Assignees {default}
    {bg_help}separator `;`{reset_bg}
    {bg_help}`-l` to list users{reset_bg}
    """.format(
                default=Fg.SUCCESS.value + ';'.join(self.__default_issue.assignees) + Fg.RESET.value + ' :' if len(
                    self.__default_issue.assignees) else '',
                reset_bg=Fg.RESET.value,
                bg_help=Fg.NOTICE.value
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
    """.format(fg_cyan=Fg.NOTICE.value,
               members=' | '.join(members),
               reset_fg=Fg.RESET.value
               )
                else:
                    message: str = Fg.FAIL.value + 'No member, type `abort`' + Fg.RESET.value
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
            title = input(Fg.FAIL.value + '[required]' + Fg.RESET.value + ' Title : ')
            milestone.title = title

        description: str = input('Description : ')
        if description:
            milestone.description = description

        return milestone

    def __resume_milestone(self, milestone: Dict[str, str]) -> Create:
        print(
            """###############################################
################ {green}Milestone created{reset} ################
###############################################{green}
title : {title!s}
number : {number!s}
url : {url!s}
{reset}###############################################
""".format(
                green=Fg.NOTICE.value,
                title=milestone.get('title'),
                number=milestone.get('number'),
                url=milestone.get('html_url'),
                reset=Fg.RESET.value
            )
        )
        return self

    def __input_milestone(self, issue: IssueGithub) -> Create:

        milestone: str = input(
            """Milestone number : 
{bg_help}`-l` to list the existing 
`-c` to create milestone{reset_bg}""".format(
                reset_bg=Fg.RESET.value,
                bg_help=Fg.NOTICE.value
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
                    fg_cyan=Fg.NOTICE.value,
                    milestones=' | '.join(milestones_repo),
                    fg_reset=Fg.RESET.value
                )
            else:
                message: str = Fg.FAIL.value + 'No milestone, type `-c` to create milestone or `-a` for abort' + Fg.RESET.value

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
        labels_lst: List[str]

        if self.__options.get('default') is not None:
            labels_lst = self.__default_issue.labels
        else:
            message: str = 'Labels '
            r: Response = self.__github.get_labels()

            labels_repo: List[str] = []
            if r.status_code is 200:
                labels_response: List[Dict[str, str]] = r.json()
                l: Dict[str, str]
                for l in labels_response:
                    labels_repo.append(l.get('name'))

            default: str = ';'.join(self.__default_issue.labels) if len(
                self.__default_issue.assignees) else ''

            if len(labels_repo):
                message += """
    {fg_cyan}{labels!s}{fg_reset}
    
    Choose label : {fg_green}{default}{fg_reset}
    {fg_cyan}separator `;` {fg_reset}
    """.format(
                    fg_cyan=Fg.NOTICE.value,
                    labels=' | '.join(labels_repo),
                    fg_reset=Fg.RESET.value,
                    fg_green=Fg.SUCCESS.value,
                    default=default
                )

            labels: str = input(message)
            labels = labels if len(labels) > 0 else default
            labels_lst = labels.split(';')
            labels_lst = self.__sanitize_list_input(labels_lst)

        if len(labels_lst):
            issue.labels = labels_lst
        return self

    def __input_issue(self):
        issue: IssueGithub = IssueGithub()
        title: str = ''

        title_default: str = Fg.SUCCESS.value + self.__default_issue.title + Fg.RESET.value if self.__default_issue.title is not None else ''

        if self.__options.get('default') is not None and title_default != '':
            title = title_default
        else:
            while not len(title) > 0:

                title = input(Fg.FAIL.value + '[required]' + Fg.RESET.value + ' Title : ' + title_default)
                title = title if title else self.__default_issue.title

        issue.title = title

        if self.__options.get('default') is None:
            body: str = input('Description : ')
            if body:
                issue.body = body

        self.__input_assignees(issue).__input_labels(issue)

        return issue

    def __post_issue(self, issue: IssueGithub) -> Response:
        Log.info('waiting... Github create issue')
        return self.__github.create_issue(issue)

    def __resume_issue(self, issue: IssueGithub) -> Create:
        CommonIssue.print_resume_issue(issue)
        return self

    def __resume_issue_created(self, issue: IssueGithub) -> Create:
        CommonIssue.print_resume_issue(issue)
        return self

    def process(self) -> Issue:
        self.__start_message()

        self.__start_message_issue()

        issue: IssueGithub = self.__input_issue()

        r: Response = self.__post_issue(issue)

        if r.status_code is 201:
            issue_created: IssueGithub = IssueGithub.from_api_dict(r.json())

            self.__resume_issue_created(issue_created)
        else:
            raise GithubRequestApiError(r)

        return issue_created
