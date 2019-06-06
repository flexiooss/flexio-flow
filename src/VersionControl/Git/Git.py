from __future__ import annotations

from typing import Optional

from VersionControl.Git.Actions.CommitHandler import CommitHandler
from VersionControl.CommitHandler import CommitHandler as AbstractCommitHandler
from VersionControl.Git.GitCmd import GitCmd
from VersionControl.Git.IssueHandler import IssueHandler
from VersionControl.Git.TopicHandler import TopicHandler
from VersionControl.VersionControl import VersionControl
from VersionControl.Branch import Branch
from VersionControl.Git.Branches.BranchBuilder import BranchBuilder
from Branches.Branches import Branches
from VersionControl.Commit import Commit as CommitValueObject


class Git(VersionControl):

    def build_branch(self, branch: Branches) -> Branch:
        branch_inst: Branch = BranchBuilder.create(branch, self.state_handler)
        return branch_inst

    def feature(self) -> Branch:
        branch_inst: Branch = BranchBuilder.create(Branches.FEATURE, self.state_handler)
        return branch_inst

    def hotfix(self) -> Branch:
        branch_inst: Branch = BranchBuilder.create(Branches.HOTFIX, self.state_handler)
        return branch_inst

    def master(self) -> Branch:
        branch_inst: Branch = BranchBuilder.create(Branches.MASTER, self.state_handler)
        return branch_inst

    def release(self) -> Branch:
        branch_inst: Branch = BranchBuilder.create(Branches.RELEASE, self.state_handler)
        return branch_inst

    def get_issue_number(self) -> Optional[int]:
        issue_number: Optional[int] = IssueHandler(self.state_handler).number_from_branch_name()
        return issue_number

    def get_topic_number(self) -> Optional[int]:
        topic_number: Optional[int] = TopicHandler(self.state_handler).number_from_branch_name()
        return topic_number

    def commit(self, commit: CommitValueObject) -> AbstractCommitHandler:
        return CommitHandler(self.state_handler).with_commit(commit)

    def is_current_branch_develop(self) -> bool:
        return GitCmd(self.state_handler).get_current_branch_name() == Branches.DEVELOP.value
