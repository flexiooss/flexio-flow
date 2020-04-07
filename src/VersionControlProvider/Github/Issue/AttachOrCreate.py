from __future__ import annotations
from typing import List, Dict, Type, Optional
from requests import Response
from Core.ConfigHandler import ConfigHandler
from Log.Log import Log
from VersionControlProvider.Github.Github import Github
from VersionControlProvider.Github.GithubRequestApiError import GithubRequestApiError
from VersionControlProvider.Github.Issue.CommonIssue import CommonIssue
from VersionControlProvider.Github.Issue.Create import Create
from VersionControlProvider.Github.Ressources.IssueGithub import IssueGithub
from VersionControlProvider.Github.Repo import Repo
from VersionControlProvider.Github.Ressources.Milestone import Milestone
from VersionControlProvider.Issue import Issue
from ConsoleColors.Fg import Fg
from VersionControlProvider.IssueDefault import IssueDefault


class AttachOrCreate:

    def __init__(self, config_handler: ConfigHandler, repo: Repo, default_issue: Optional[IssueDefault], options: Optional[Dict[str, str]]):
        self.__config_handler: ConfigHandler = config_handler
        self.__repo: Repo = repo
        self.__github = Github(self.__config_handler).with_repo(self.__repo)
        self.__default_issue: Optional[IssueDefault] = default_issue
        self.__options: Optional[Dict[str, str]] = options
        self.__issue: Optional[Issue] = None

    def __would_attach_issue(self) -> bool:
        if self.__options.get('default') is not None:
            return False
        else:
            issue: str = input("""Have already an issue y/{green}n{reset_fg} : """.format(
                green=Fg.SUCCESS.value,
                reset_fg=Fg.RESET.value,
            ))
            issue = issue if issue else 'n'
            return issue == 'y'

    def __number_issue(self) -> int:
        issue: str = input('Issue number : ')
        return int(issue)

    def __read_issue(self, issue: IssueGithub) -> Response:
        return self.__github.read_issue(issue)

    def __attach(self) -> bool:
        if self.__would_attach_issue():
            issue_number = self.__number_issue()
            issue: IssueGithub = IssueGithub().with_number(issue_number)

            try:
                Log.info('waiting... from Github... Issue : ' + str(issue_number))

                r: Response = self.__read_issue(issue)
                self.__issue: IssueGithub = IssueGithub.from_api_dict(r.json())
                CommonIssue.print_resume_issue(self.__issue)
            except FileNotFoundError:
                Log.error(Fg.FAIL.value + 'Issue not found : retry' + Fg.RESET.value)
                return self.process()

            return True
        else:
            return False

    def __create(self) -> Issue:
        return Create(
            config_handler=self.__config_handler,
            repo=self.__repo,
            default_issue=self.__default_issue,
            options=self.__options
        ).process()

    def process(self) -> Issue:
        if self.__options.get('default') is None:
            CommonIssue.issuer_message()

        if self.__attach():
            return self.__issue
        else:
            return self.__create()
