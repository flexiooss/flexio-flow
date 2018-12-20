from __future__ import annotations

from typing import Type

from FlexioFlow.Actions.Action import Action
from FlexioFlow.Actions.Actions import Actions
from VersionControlProvider.Issuer import Issuer
from VersionControlProvider.IssuerFactory import IssuerFactory
from VersionControlProvider.Issuers import Issuers


class Start(Action):
    def process(self):
        if self.config_handler.has_issuer():
            issuer: Issuers = Issuers.GITHUB
            issuer: Type[Issuer] = IssuerFactory.build(self.config_handler, issuer)
            issuer.create()

        # self.version_control.with_branch(self.branch).set_action(Actions.START).process()
