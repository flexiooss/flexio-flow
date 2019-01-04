from typing import Optional

from Branches.BranchHandler import BranchHandler
from FlexioFlow.StateHandler import StateHandler
from VersionControl.GitFlow.GitCmd import GitCmd


class IssueHandler:
    def __init__(self, state_handler: StateHandler):
        self.__state_handler: StateHandler = state_handler
        self.__git: GitCmd = GitCmd(self.__state_handler)

    def number_from_branch_name(self) -> Optional[int]:
        branch_name: str = self.__git.get_current_branch_name()
        return BranchHandler.issue_number_from_branch_name(branch_name)
