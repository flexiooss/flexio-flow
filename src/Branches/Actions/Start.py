from __future__ import annotations

from typing import Type

from Branches.Actions.Action import Action
from Branches.Actions.Actions import Actions
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Issuer import Issuer
from VersionControlProvider.IssuerFactory import IssuerFactory
from VersionControlProvider.Issuers import Issuers


class Start(Action):
    def process(self):
        if self.config_handler.has_issuer():
            issuer: Issuers = Issuers.GITHUB
            issuer: Type[Issuer] = IssuerFactory.build(self.state_handler, self.config_handler, issuer)
            issue: Issue = issuer.create()
            self.version_control.build_branch(self.branch).with_issue(issue).with_action(Actions.START).process()
        else:
            self.version_control.build_branch(self.branch).with_action(Actions.START).process()
