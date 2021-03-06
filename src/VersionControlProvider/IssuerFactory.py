from __future__ import annotations

from Core.ConfigHandler import ConfigHandler
from FlexioFlow.Options import Options
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider import Issuer
from VersionControlProvider.Github.GithubIssuer import GithubIssuer
from VersionControlProvider.Issuers import Issuers


class IssuerFactory:

    @staticmethod
    def build(
            state_handler: StateHandler,
            config_handler: ConfigHandler,
            issuer: Issuers,
            options: Options
    ) -> Issuer:
        if issuer is Issuers.GITHUB:
            return GithubIssuer(state_handler, config_handler,options)

        raise NotImplementedError
