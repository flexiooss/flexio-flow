from __future__ import annotations

from Core.ConfigHandler import ConfigHandler
from Branches.Actions.Actions import Actions
from Branches.Actions.Action import Action
from Branches.Actions.Init import Init
from Branches.Actions import Start
from Branches.Actions import Finish
from Branches.Actions.PreCheck import PreCheck
from typing import Type, Dict, Optional
from Branches.Branches import Branches
from VersionControl.VersionControl import VersionControl
from FlexioFlow.StateHandler import StateHandler


class ActionFactory:

    @staticmethod
    def build(
            action: Actions,
            version_control: Type[VersionControl],
            branch: Optional[Branches],
            state_handler: StateHandler,
            options: Dict[str, str],
            config_handler: ConfigHandler
    ) -> Action:

        if action is Actions.INIT:
            return Init(version_control, branch, state_handler, options, config_handler)

        if action is Actions.START:
            return Start(version_control, branch, state_handler, options, config_handler)

        if action is Actions.FINISH:
            return Finish(version_control, branch, state_handler, options, config_handler)

        if action is Actions.PRECHECK:
            return PreCheck(version_control, branch, state_handler, options, config_handler)

        raise ValueError("Bad ActionFactory creation: " + action.value)
