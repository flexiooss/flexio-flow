from __future__ import annotations

from typing import Optional, Dict

from Branches.Actions.Issuer.IssueDefaultBuilder import IssueDefaultBuilder
from Branches.Branches import Branches
from Core.ConfigHandler import ConfigHandler
from Core.IssuerHandler import IssuerHandler
from FlexioFlow.Options import Options
from FlexioFlow.StateHandler import StateHandler
from Log.Log import Log
from VersionControl.VersionControl import VersionControl
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Issuer import Issuer
from VersionControlProvider.Topic import Topic


class IssueBuilder:
    def __init__(self,
                 version_control: VersionControl,
                 state_handler: StateHandler,
                 config_handler: ConfigHandler,
                 branch: Optional[Branches],
                 options: Options
                 ):
        self.__version_control: VersionControl = version_control
        self.__state_handler: StateHandler = state_handler
        self.__config_handler: ConfigHandler = config_handler
        self.__options: Options = options
        self.__branch: Optional[Branches] = branch
        self.__issue: Optional[Issue] = None
        self.__issuer: Optional[Issuer] = IssuerHandler(
            self.__state_handler, self.__config_handler, self.__options
        ).issuer()

    def try_ensure_issue(self) -> IssueBuilder:
        if self.__config_handler.has_issuer() and self.__issuer is not None and self.__issuer.has_repo() and self.__branch is not None:

            self.__issue = self.__issuer.attach_or_create(
                default_issue=IssueDefaultBuilder().build(
                    self.__state_handler,
                    self.__config_handler,
                    self.__branch,
                    self.__options
                ),
                options=self.__options
            )
        return self

    def find_issue_from_branch_name(self) -> IssueBuilder:
        if self.__issuer is not None:
            issue_number: Optional[int] = self.__version_control.get_issue_number()

            if issue_number is not None:
                self.__issue = self.__issuer.issue_builder().with_number(issue_number)
                if self.__issue is not None:
                    Log.info('Issue number ' + str(self.__issue.number) + ' found')
            else:
                Log.info('No Issue found')
        return self

    def comment_issue_with_topic(self, topic: Topic) -> IssueBuilder:
        if self.__issue is not None:
            Log.info('Waiting... Comment issue with topics : ' + str(topic.number))
            self.__issuer.comment(self.__issue, 'Topic : ' + topic.url())

        return self

    def issue(self) -> Optional[Issue]:
        return self.__issue

    def issuer(self) -> Optional[Issuer]:
        return self.__issuer
