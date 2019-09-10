from __future__ import annotations

from typing import Optional, Type, Dict, Union

from Core.ConfigHandler import ConfigHandler
from Core.Core import Core
from Exceptions.NoIssuerConfigured import NoIssuerConfigured
from Exceptions.NoTopicerConfigured import NoTopicerConfigured
from FlexioFlow.Actions.Issue import Issue
from FlexioFlow.Actions.IssueActions import IssueActions
from FlexioFlow.Actions.Topic import Topic
from FlexioFlow.Actions.TopicActions import TopicActions
from FlexioFlow.StateHandler import StateHandler
from Branches.Actions.Actions import Actions as BranchActions
from Branches.Actions.Action import Action
from Branches.Branches import Branches
from Branches.Actions.ActionBuilder import ActionBuilder
from FlexioFlow.Subject import Subject
from PoomCiDependency.PoomCiDependency import PoomCiDependency
from Schemes.Schemes import Schemes
from VersionControl.VersionController import VersionController
from VersionControl.VersionControl import VersionControl
from VersionControl.VersionControlBuilder import VersionControlBuilder
from pathlib import Path
from FlexioFlow.Actions.Version import Version
from FlexioFlow.Actions.Convert import Convert
from Core.Actions.Actions import Actions as ActionsCore
from PoomCiDependency.Actions.Actions import Actions as PoomCiActions


class FlexioFlow:
    __branch: Optional[Branches] = None
    __branch_action: Optional[BranchActions] = None
    __config_handler: ConfigHandler
    __core_action: Optional[ActionsCore] = None
    __poom_ci_actions: Optional[PoomCiActions] = None
    __dir_path: Path
    __issue_action: Optional[IssueActions] = None
    __topic_action: Optional[TopicActions] = None
    __options: Dict[str, Union[str, Schemes, bool]]
    __state_handler: Optional[StateHandler] = None
    __version_controller: VersionController
    __version_control: VersionControl = None

    def __init__(self, subject: Subject):
        self.subject: Subject = subject

    def set_environment(self,
                        version_controller: VersionController,
                        branch_action: Optional[BranchActions],
                        core_action: Optional[ActionsCore],
                        issue_action: Optional[IssueActions],
                        topic_action: Optional[TopicActions],
                        poom_ci_actions: Optional[PoomCiActions],
                        branch: Optional[Branches],
                        options: Dict[str, Union[str, Schemes, bool]],
                        dir_path: Path,
                        config_handler: ConfigHandler
                        ) -> FlexioFlow:

        self.__version_controller: VersionController = version_controller

        self.__branch_action: Optional[BranchActions] = branch_action
        self.__issue_action: Optional[IssueActions] = issue_action
        self.__topic_action: Optional[TopicActions] = topic_action
        self.__core_action: Optional[ActionsCore] = core_action
        self.__poom_ci_actions: Optional[PoomCiActions] = poom_ci_actions
        self.__branch: Optional[Branches] = branch
        self.__options: Dict[str, Union[str, Schemes, bool]] = options

        if not dir_path.is_dir():
            raise NotADirectoryError

        self.__dir_path: Path = dir_path
        self.__config_handler: ConfigHandler = config_handler
        return self

    def __ensure_state_handler(self):
        if self.__state_handler is None:
            self.__state_handler = StateHandler(self.__dir_path)
            if self.__branch_action not in [BranchActions.INIT]:
                self.__state_handler.load_file_config()

    def __ensure_version_control(self):
        self.__ensure_state_handler()
        if self.__version_control is None:
            self.__version_control: VersionControl = VersionControlBuilder.build(
                self.__version_controller,
                self.__state_handler
            )

    def __ensure_config_handler(self):
        self.__config_handler.load_file_config()

    def __process_subject_core(self):
        if self.__core_action is None:
            raise ValueError('should have Action')

        Core(
            action=self.__core_action,
            options=self.__options,
            config_handler=self.__config_handler
        ).process()

    def __process_subject_version(self):
        self.__ensure_state_handler()

        Version(
            state_handler=self.__state_handler,
            options=self.__options
        ).process()

    def __process_subject_convert(self):
        self.__ensure_state_handler()

        Convert(
            options=self.__options
        ).process()

    def __process_subject_issue(self):
        if self.__issue_action is None:
            raise ValueError('should have Action')

        self.__ensure_state_handler()
        self.__ensure_version_control()
        self.__ensure_config_handler()

        if not self.__config_handler.has_issuer():
            raise NoIssuerConfigured()

        Issue(
            action=self.__issue_action,
            state_handler=self.__state_handler,
            version_control=self.__version_control,
            config_handler=self.__config_handler,
            options=self.__options
        ).process()

    def __process_subject_topic(self):
        if self.__topic_action is None:
            raise ValueError('should have Action')

        self.__ensure_state_handler()
        self.__ensure_version_control()
        self.__ensure_config_handler()

        if not self.__config_handler.has_topicer():
            raise NoTopicerConfigured()

        Topic(
            action=self.__topic_action,
            state_handler=self.__state_handler,
            version_control=self.__version_control,
            config_handler=self.__config_handler,
            options=self.__options
        ).process()

    def __process_branch_action(self):
        if self.__branch_action is None:
            raise ValueError('should have Action')

        self.__ensure_state_handler()
        self.__ensure_version_control()
        self.__ensure_config_handler()

        self.__ensure_precheck()

        ActionBuilder.build(
            action=self.__branch_action,
            version_control=self.__version_control,
            branch=self.__branch,
            state_handler=self.__state_handler,
            options=self.__options,
            config_handler=self.__config_handler
        ).process()

    def __process_poom_ci(self):
        if self.__poom_ci_actions is None:
            raise ValueError('should have Action')

        self.__ensure_state_handler()

        PoomCiDependency(
            action=self.__poom_ci_actions,
            state_handler=self.__state_handler,
            options=self.__options
        ).process()

    def __ensure_precheck(self):
        if self.__branch_action == BranchActions.FINISH and self.__branch == Branches.RELEASE:
            ActionBuilder.build(
                action=BranchActions.PRECHECK,
                version_control=self.__version_control,
                branch=self.__branch,
                state_handler=self.__state_handler,
                options=self.__options,
                config_handler=self.__config_handler
            ).process()

    def process(self):
        if self.subject is Subject.CORE:
            self.__process_subject_core()

        elif self.subject is Subject.VERSION:
            self.__process_subject_version()

        elif self.subject is Subject.CONVERT:
            self.__process_subject_convert()

        elif self.subject is Subject.ISSUE:
            self.__process_subject_issue()

        elif self.subject is Subject.TOPICS:
            self.__process_subject_topic()

        elif self.subject is Subject.BRANCH:
            self.__process_branch_action()

        elif self.subject is Subject.POOM_CI:
            self.__process_poom_ci()

        else:
            raise NotImplementedError()
