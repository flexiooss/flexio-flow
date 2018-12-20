from __future__ import annotations
import abc
from typing import Optional, Type

from FlexioFlow.Actions.Actions import Actions
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.Issue import Issue


class Branch(abc.ABC):
    action: Actions

    def __init__(self, state_handler: StateHandler) -> None:
        self.state_handler: StateHandler = state_handler
        self.issue: Optional[Type[Issue]] = None

    def with_issue(self, issue: Type[Issue]) -> Branch:
        self.issue = issue
        return self

    @abc.abstractmethod
    def process(self):
        pass

    def with_action(self, action: Actions) -> Branch:
        self.action: Actions = action
        return self

    def start_message(self, message: str):
        print(
            """####################################################
{message!s}           
####################################################
""".format(message=message))
