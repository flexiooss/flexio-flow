from __future__ import annotations
import getopt
import re
import sys
from pathlib import Path

from typing import Tuple, List, Optional, Dict, Union

from Branches.Actions.Actions import Actions
from Branches.Branches import Branches
from Core.ConfigHandler import ConfigHandler
from Core.Core import Core
from ExecutorConfig import ExecutorConfig
from FlexioFlow.Actions.IssueActions import IssueActions
from FlexioFlow.Actions.TopicActions import TopicActions
from FlexioFlow.Options import Options
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.Task import Task
from FlexioFlow.options.Resolver import Resolver
from PoomCiDependency.Actions.Actions import Actions as PoomCiActions
from Core.Actions.Actions import Actions as ActionsCore
from VersionControl.VersionController import VersionController


class Executor:
    __argv: List[str] = []
    __config: ExecutorConfig = ExecutorConfig()

    def __init__(self, cwd: Path) -> None:
        self.__cwd: Path = cwd
        self.__options_resolver: Resolver = Resolver()

    def __extract_options(self):
        options: Options = Options()

        try:
            opts, args = getopt.gnu_getopt(
                self.__argv,
                self.__options_resolver.short_name_options(),
                self.__options_resolver.name_options()
            )

        except getopt.GetoptError:
            print('OUPS !!!')
            print('Oh buddy try `flexio-flow -H`')
            sys.exit(2)

        for opt, arg in opts:
            self.__options_resolver.resolve(opt=opt, arg=arg, options=options)

        self.__config.options = options

    def __extract_task_action(self) -> Executor:
        arg: str
        for arg in self.__argv:
            arg = re.sub('[\s+]', '', arg).lower()

            if Actions.has_value(arg):
                self.__config.branch_action = Actions[arg.upper()]
            if Branches.has_value(arg):
                self.__config.branch = Branches[arg.upper().replace('-', '_')]
            if Task.has_value(arg):
                self.__config.task = Task[arg.upper().replace('-', '_')]
            if ActionsCore.has_value(arg):
                self.__config.core_action = ActionsCore[arg.upper().replace('-', '_')]
            if IssueActions.has_value(arg) or TopicActions.has_value(arg):
                self.__config.issue_action = IssueActions[arg.upper().replace('-', '_')]
            if TopicActions.has_value(arg):
                self.__config.topic_action = TopicActions[arg.upper().replace('-', '_')]
            if PoomCiActions.has_value(arg):
                self.__config.poom_ci_actions = PoomCiActions[arg.upper().replace('-', '_')]

        return self

    def __ensure_version_dir(self):
        version_dir: Path
        if self.__config.options.version_dir:
            version_dir = Path(str(self.__config.options.version_dir))
        else:
            file_dir: Optional[Path] = StateHandler.find_file_version(self.__cwd)
            if file_dir is not None:
                version_dir = file_dir
            else:
                version_dir = self.__cwd

        self.__config.version_dir = version_dir

    def __ensure_tasks(self):
        self.__config.task = Task.BRANCH if self.__config.task is None else self.__config.task

    def __ensure_config_handler(self):
        self.__config.config_handler = ConfigHandler(Core.CONFIG_DIR, self.__config.options.config)

    def __ensure_version_controller(self):
        self.__config.version_controller = VersionController.GIT

    def exec(self, argv: List[str]) -> Executor:
        self.__argv = argv
        self.__extract_options()
        self.__ensure_version_dir()
        self.__extract_task_action()
        self.__ensure_tasks()
        self.__ensure_config_handler()
        self.__ensure_version_controller()
        return self

    def config(self) -> ExecutorConfig:
        return self.__config
