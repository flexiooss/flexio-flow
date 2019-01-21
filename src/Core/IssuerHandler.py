from typing import Optional

from Core.ConfigHandler import ConfigHandler
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.Issuer import Issuer
from VersionControlProvider.IssuerFactory import IssuerFactory
from VersionControlProvider.Issuers import Issuers


class IssuerHandler:
    def __init__(self, state_handler: StateHandler, config_handler: ConfigHandler):
        self.state_handler: StateHandler = state_handler
        self.config_handler: ConfigHandler = config_handler

    def issuer(self) -> Optional[Issuer]:
        issuers: Issuers = Issuers.GITHUB
        issuer = None

        try:
            issuer: Issuer = IssuerFactory.build(self.state_handler, self.config_handler, issuers)
        except ValueError:
            print('Can\'t get Issuer')
        finally:
            return issuer
