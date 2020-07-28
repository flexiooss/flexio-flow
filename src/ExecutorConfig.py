from typing import Optional

from Core.ConfigHandler import ConfigHandler
from FlexioFlow.Actions.IssueActions import IssueActions
from FlexioFlow.Actions.TopicActions import TopicActions
from Branches.Actions.Actions import Actions
from Core.Actions.Actions import Actions as ActionsCore
from FlexioFlow.Options import Options
from FlexioFlow.Task import Task
from Branches.Branches import Branches
from pathlib import Path

from VersionControl.VersionController import VersionController
from PoomCiDependency.Actions.Actions import Actions as PoomCiActions


class ExecutorConfig:
    branch_action: Optional[Actions] = None
    branch: Optional[Branches] = None
    task: Optional[Task] = None
    core_action: Optional[ActionsCore] = None
    options: Options
    version_dir: Path
    issue_action: Optional[IssueActions] = None
    topic_action: Optional[TopicActions] = None
    version_controller: VersionController
    poom_ci_actions: Optional[PoomCiActions] = None
    config_handler: ConfigHandler
