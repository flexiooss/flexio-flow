from __future__ import annotations

from Exceptions.NoIssue import NoIssue
from Exceptions.NoIssuerConfigured import NoIssuerConfigured
from FlexioFlow.Version import Version
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from typing import List, Type, Optional
from Branches.Actions.Action import Action
from Branches.Actions.Actions import Actions
from Branches.Branches import Branches
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Issuer import Issuer
from VersionControlProvider.IssuerFactory import IssuerFactory
from VersionControlProvider.Issuers import Issuers


class Commit(Action):

    def __start_message(self) -> Commit:
        print(
            """###############################################
################# Flexio FLow #################
###############################################
#################    Commit     #################
""")
        return self

    def __input_version(self) -> Commit:
        version: str = input('Version (0.0.0) : ')
        self.state_handler.state.version = Version.from_str(version if version else '0.0.0')
        return self

    def __final_message(self) -> Commit:
        print(
            """###############################################
Enjoy with Flexio FLow 
###############################################
""")
        return self

    def process(self):


        if self.config_handler.has_issuer():
            issuer: Issuers = Issuers.GITHUB
            issuer: Type[Issuer] = IssuerFactory.build(self.state_handler, self.config_handler, issuer)
            issue_number: Optional[int] = self.version_control.get_issue_number()
            if issue_number is None:
                raise NoIssue()
            else:
                self.__start_message()
        else:
            self.version_control.commit()

        self.__final_message()
