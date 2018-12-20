from typing import List, Type

from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Github.Issue.GithubIssuer import GithubIssuer
from VersionControlProvider.Issuer import Issuer


class IssuerHandler:
    @staticmethod
    def issuers_from_config_handler(config_handler: ConfigHandler) -> List[Type[Issuer]]:
        ret: list = []
        if config_handler.config.github.activate is True:
            ret.append(GithubIssuer(config_handler))
        return ret
