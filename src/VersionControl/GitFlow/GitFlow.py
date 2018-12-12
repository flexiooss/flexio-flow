from __future__ import annotations

from pathlib import Path
from subprocess import Popen, PIPE

from VersionControl.VersionControl import VersionControl
from VersionControl.Branch import Branch
from typing import Type
from VersionControl.GitFlow.Branches.BranchFactory import BranchFactory
from VersionControl.Branches import Branches


class GitFlow(VersionControl):
    REMOTE: str = 'origin'

    def master(self) -> Branch:
        branch: Branch = BranchFactory.create(Branches.MASTER, self.state_handler)
        return branch

    def hotfix(self) -> Branch:
        branch: Branch = BranchFactory.create(Branches.HOTFIX, self.state_handler)
        return branch

    def release(self) -> Branch:
        branch: Branch = BranchFactory.create(Branches.RELEASE, self.state_handler)
        return branch

    def with_branch(self, branch: Branches) -> Branch:
        branch: Branch = BranchFactory.create(branch, self.state_handler)
        return branch

    @classmethod
    def remote_tag_exists(cls, tag: str, dir_path: Path) -> bool:
        stdout, stderr = Popen([
            'git',
            'ls-remote',
            cls.REMOTE,
            'refs/tags/' + tag
        ], stdout=PIPE, cwd=dir_path.as_posix()).communicate()
        print(stdout.strip())
        return len(stdout.strip()) > 0

    @classmethod
    def init_config(cls):
        Popen(["git", "flow", "init", "-f", "-d"]).communicate()
