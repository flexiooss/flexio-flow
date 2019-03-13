from __future__ import annotations
import abc
from typing import Optional

from Branches.Actions.Actions import Actions
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.Issue import Issue


class Branch(abc.ABC):
    action: Actions
    issue: Optional[Issue]
    name: Optional[str]

    def __init__(self, state_handler: StateHandler) -> None:
        self.state_handler: StateHandler = state_handler
        self.issue: Optional[Issue] = None
        self.name: Optional[str] = None

    def with_issue(self, issue: Issue) -> Branch:
        self.issue = issue
        return self

    def with_name(self, name: str) -> Branch:
        self.name = name
        return self

    @abc.abstractmethod
    def process(self):
        pass

    def with_action(self, action: Actions) -> Branch:
        self.action: Actions = action
        return self

    def start_message(self, message: str):
        print("""
####################################################
{message!s}           
####################################################
""".format(message=message))
