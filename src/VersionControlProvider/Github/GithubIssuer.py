from VersionControlProvider.Issuer import Issuer


class GithubIssuer(Issuer):
    def create(self) -> str:
        print('create issue')
        pass
