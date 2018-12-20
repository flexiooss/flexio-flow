from __future__ import annotations

from Core.ConfigHandler import ConfigHandler
from VersionControlProvider import Issuer
from VersionControlProvider.Github.GithubIssuer import GithubIssuer
from VersionControlProvider.Issuers import Issuers


class IssuerFactory:

    @staticmethod
    def build(
            config_handler: ConfigHandler,
            issuer: Issuers
    ) -> Issuer:
        if issuer is Issuers.GITHUB:
            return GithubIssuer(config_handler)

        raise NotImplementedError
