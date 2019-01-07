from Core.ConfigHandler import ConfigHandler
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.Issuer import Issuer
from VersionControlProvider.IssuerFactory import IssuerFactory
from VersionControlProvider.Issuers import Issuers


class IssuerHandler:
    def __init__(self, state_handler: StateHandler, config_handler: ConfigHandler):
        self.state_handler: StateHandler = state_handler
        self.config_handler: ConfigHandler = config_handler

    def issuer(self) -> Issuer:
        issuer: Issuers = Issuers.GITHUB
        issuer: Issuer = IssuerFactory.build(self.state_handler, self.config_handler, issuer)
        return issuer
