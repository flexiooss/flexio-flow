from VersionControl.GitFlow.GitCmd import GitCmd
from VersionControlProvider.Github.Issue.Create import Create
from VersionControlProvider.Github.Repo import Repo
from VersionControlProvider.Issuer import Issuer


class GithubIssuer(Issuer):
    def create(self):
        print('create issue')

        repo: Repo = Repo(owner='flexiooss', repo='flexio-flow-punching-ball')
        # repo: Repo = GitCmd(self.state_handler).get_repo()

        Create(self.config_handler, repo).process()
