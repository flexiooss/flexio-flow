from typing import Type

from VersionControlProvider.Github.Issue.Create import Create
from VersionControlProvider.Github.Ressources.IssueGithub import IssueGithub
from VersionControlProvider.Github.Repo import Repo
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Issuer import Issuer


class GithubIssuer(Issuer):
    def create(self) -> Type[Issue]:
        print('create issue')

        repo: Repo = Repo(owner='flexiooss', repo='flexio-flow-punching-ball')
        # repo: Repo = GitCmd(self.state_handler).get_repo()

        return Create(self.config_handler, repo).process()
