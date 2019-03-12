from __future__ import annotations
from typing import Type, Optional
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.Issue import Issue


class PreCheck:
    def __init__(self, state_handler: StateHandler, issue: Optional[Type[Issue]]):
        self.__state_handler: StateHandler = state_handler
        self.__issue: Optional[Type[Issue]] = issue

    def process(self):
        print('Not implemented yet')
