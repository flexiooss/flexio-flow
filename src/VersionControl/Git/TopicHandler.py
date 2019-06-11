from typing import Optional, List

from Branches.BranchHandler import BranchHandler
from FlexioFlow.StateHandler import StateHandler
from VersionControl.Git.GitCmd import GitCmd


class TopicHandler:
    def __init__(self, state_handler: StateHandler):
        self.__state_handler: StateHandler = state_handler
        self.__git: GitCmd = GitCmd(self.__state_handler)

    def numbers_from_branch_name(self) -> Optional[List[int]]:
        branch_name: str = self.__git.get_current_branch_name()
        return BranchHandler.topics_number_from_branch_name(branch_name)
