from __future__ import annotations
from FlexioFlow.Actions.Actions import Actions
from FlexioFlow.Actions.Action import Action
from FlexioFlow.Actions.Start import Start
from FlexioFlow.Actions.Finish import Finish
from FlexioFlow.Actions.Plan import Plan
from typing import Type, Dict, Optional
from VersionControl.Branches import Branches
from VersionControl.VersionControl import VersionControl
from FlexioFlow.StateHandler import StateHandler


class ActionFactory:

    @staticmethod
    def create(
            action: Actions,
            version_control: Type[VersionControl],
            branch: Optional[Branches],
            state_handler: StateHandler,
            options: Dict[str, str]
    ) -> Type[Action]:

        if action is Actions.START:
            return Start(version_control, branch, state_handler, options)

        if action is Actions.FINISH:
            return Finish(version_control, branch, state_handler, options)

        if action is Actions.PLAN:
            return Plan(version_control, branch, state_handler, options)

        raise ValueError("Bad ActionFactory creation: " + action.value)
