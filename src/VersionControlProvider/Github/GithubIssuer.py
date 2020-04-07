from typing import Type, Optional,Dict

from requests import Response

from VersionControl.Git.GitCmd import GitCmd
from VersionControlProvider.Github.Github import Github
from VersionControlProvider.Github.Issue.AttachOrCreate import AttachOrCreate
from VersionControlProvider.Github.Issue.Create import Create
from VersionControlProvider.Github.Message import Message
from VersionControlProvider.Github.Repo import Repo
from VersionControlProvider.Github.Ressources.IssueGithub import IssueGithub
from VersionControlProvider.Issue import Issue
from VersionControlProvider.IssueDefault import IssueDefault
from VersionControlProvider.Issuer import Issuer
from VersionControlProvider.IssueMessage import IssueMessage as AbstractMessage


class GithubIssuer(Issuer):
    def create(self, default_issue: Optional[IssueDefault]) -> Issue:
        repo: Repo = GitCmd(self.state_handler).get_repo()

        return Create(self.config_handler, repo, default_issue).process()

    def attach_or_create(self, default_issue: Optional[IssueDefault], options: Optional[Dict[str, str]]) -> Issue:
        repo: Repo = GitCmd(self.state_handler).get_repo()
        return AttachOrCreate(
            config_handler=self.config_handler,
            repo=repo,
            default_issue=default_issue,
            options=options
        ).process()

    def message_builder(self, message: str, issue: Optional[Issue] = None) -> AbstractMessage:
        return Message(message, issue)

    def issue_builder(self) -> Issue:
        return IssueGithub()

    def read_issue_by_number(self, number: int) -> Issue:
        repo: Repo = GitCmd(self.state_handler).get_repo()
        # repo: Repo = Repo(owner='flexiooss', repo='flexio-flow-punching-ball')
        resp: Response = Github(self.config_handler).with_repo(repo).read_issue(IssueGithub().with_number(number))
        return IssueGithub.from_api_dict(resp.json())

    def comment(self, issue: IssueGithub, text: str) -> Issue:
        repo: Repo = GitCmd(self.state_handler).get_repo()
        resp: Response = Github(self.config_handler).with_repo(repo).create_comment(
            issue=issue,
            body=text
        )
        return IssueGithub.from_api_dict(resp.json())

    def has_repo(self) -> bool:
        has_repo: bool = False
        try:
            repo: Repo = GitCmd(self.state_handler).get_repo()
            has_repo = True
        except ValueError as e:
            print(e)
            print('GithubIssuer have not repo')
        finally:
            return has_repo
