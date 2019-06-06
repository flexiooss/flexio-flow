from __future__ import annotations
from typing import Type, Optional
from FlexioFlow.StateHandler import StateHandler
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Topic import Topic


class PreCheck:
    def __init__(self,
                 state_handler: StateHandler,
                 issue: Optional[Type[Issue]],
                 topic: Optional[Type[Topic]]
                 ):
        self.__state_handler: StateHandler = state_handler
        self.__issue: Optional[Type[Issue]] = issue
        self.__topic: Optional[Type[Topic]] = topic

    def process(self):
        print('PreCheck Not implemented yet')
