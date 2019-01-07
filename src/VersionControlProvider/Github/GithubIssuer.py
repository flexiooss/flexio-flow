from typing import Type, Optional

from VersionControlProvider.Github.Issue.Create import Create
from VersionControlProvider.Github.Message import Message
from VersionControlProvider.Github.Repo import Repo
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Issuer import Issuer
from VersionControlProvider.Message import Message as AbstractMessage


class GithubIssuer(Issuer):
    def create(self) -> Type[Issue]:
        print('create issue')

        repo: Repo = Repo(owner='flexiooss', repo='flexio-flow-punching-ball')
        # repo: Repo = GitCmd(self.state_handler).get_repo()

        return Create(self.config_handler, repo).process()

    def message_builder(self, message: str, issue: Optional[Issue] = None) -> AbstractMessage:
        return Message(message, issue)
