from __future__ import annotations

from typing import Optional

from Branches.Actions.Action import Action
from Branches.Actions.Actions import Actions
from Core.IssuerHandler import IssuerHandler
from Core.TopicerHandler import TopicerHandler
from VersionControlProvider.Issue import Issue
from VersionControlProvider.Issuer import Issuer
from VersionControlProvider.Topic import Topic
from VersionControlProvider.Topicer import Topicer


class Start(Action):

    def __process_without_issue(self):
        self.version_control.build_branch(self.branch).with_action(Actions.START).process()

    def process(self):
        if self.config_handler.has_issuer():
            issuer: Optional[Issuer] = IssuerHandler(self.state_handler, self.config_handler).issuer()

            if issuer is not None and issuer.has_repo():
                issue: Issue = issuer.create()

                if self.config_handler.has_topicer():
                    topicer: Optional[Topicer] = TopicerHandler(self.state_handler, self.config_handler).topicer()

                    if topicer is not None:
                        topic: Topic = topicer.create()
                self.version_control.build_branch(self.branch).with_issue(issue).with_action(Actions.START).process()

            else:
                self.__process_without_issue()

        else:
            self.__process_without_issue()
