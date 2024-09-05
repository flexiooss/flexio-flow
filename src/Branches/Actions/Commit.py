from __future__ import annotations

from Core.IssuerHandler import IssuerHandler
from typing import Optional
from Branches.Actions.Action import Action
from Exceptions.NoChangesInBranch import NoChangesInBranch
from VersionControl.Commit import Commit as CommitValueObject
from VersionControl.CommitHandler import CommitHandler
from VersionControlProvider.Issuer import Issuer


class Commit(Action):

    def __start_message(self) -> Commit:
        print(
            r"""###############################################
################# Flexio FLow #################
###############################################
#################    Commit     #################
""")
        return self

    def __input_message(self) -> str:
        message: str = input('Message : ')
        return message

    def __final_message(self, message: str) -> Commit:
        print(
            r"""###############################################
Commited and push with message : 
{message!s}
###############################################
""".format(message=message))
        return self

    def process(self):
        message: str = ''
        if self.options.message is None:
            message = self.__input_message()
        else:
            message = self.options.message

        if self.config_handler.has_issuer():
            issue_number: Optional[int] = self.version_control.get_issue_number()
            if issue_number is not None:
                issuer: Issuer = IssuerHandler(self.state_handler, self.config_handler, self.options).issuer()
                message = issuer.message_builder(
                    message=message,
                    issue=issuer.issue_builder().with_number(issue_number)
                ).with_ref()

        commit: CommitValueObject = CommitValueObject().with_message(message)
        commit_handler: CommitHandler = self.version_control.commit(commit=commit)

        if commit_handler.can_commit():
            commit_handler.do_commit().push()
        else:
            raise NoChangesInBranch('Can\'t commit')

        self.__final_message(message)
