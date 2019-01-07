from __future__ import annotations

from Core.IssuerHandler import IssuerHandler
from typing import Optional
from Branches.Actions.Action import Action

from VersionControlProvider.Issuer import Issuer


class Commit(Action):

    def __start_message(self) -> Commit:
        print(
            """###############################################
################# Flexio FLow #################
###############################################
#################    Commit     #################
""")
        return self

    def __input_message(self) -> str:
        message: str = input('Message : ')
        return message

    def __final_message(self, message:str) -> Commit:
        print(
            """###############################################
Commited with message : 
{message!s}
###############################################
""".format(message=message))
        return self

    def process(self):

        message: str = self.__input_message()

        if self.config_handler.has_issuer():
            issue_number: Optional[int] = self.version_control.get_issue_number()
            if issue_number is not None:
                issuer: Issuer = IssuerHandler(self.state_handler, self.config_handler).issuer()
                message = issuer.message_builder(
                    message=message,
                    issue=issuer.create().with_number(issue_number)
                )

        self.version_control.commit(message=message)

        self.__final_message(message)
