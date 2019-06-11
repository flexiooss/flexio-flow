from __future__ import annotations
import abc
from typing import Optional, Dict, List

from Branches.Actions.Actions import Actions
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic


class Branch(abc.ABC):
    action: Actions
    issue: Optional[Issue]
    topics: Optional[Topic]
    name: Optional[str]

    def __init__(self, state_handler: StateHandler) -> None:
        self.state_handler: StateHandler = state_handler
        self.issue: Optional[Issue] = None
        self.topics: Optional[List[Topic]] = None
        self.name: Optional[str] = None
        self.options: Dict[str, str] = {}

    def with_issue(self, issue: Issue) -> Branch:
        self.issue = issue
        return self

    def with_topics(self, topics: Optional[List[Topic]]) -> Branch:
        self.topics = topics
        return self

    def with_name(self, name: str) -> Branch:
        self.name = name
        return self

    def with_options(self, options: Dict[str, str]) -> Branch:
        self.options = options
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
