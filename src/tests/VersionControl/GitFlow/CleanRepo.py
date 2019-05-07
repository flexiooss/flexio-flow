import unittest
from typing import List

from FlexioFlow.StateHandler import StateHandler
from VersionControl.Git.GitCmd import GitCmd
from tests.VersionControl.GitFlow.TestGitFlowHelper import TestGitFlowHelper


class CleanRepo(unittest.TestCase):

    def test_clean(self):
        TestGitFlowHelper.mount_workdir_and_clone()

        git: GitCmd = GitCmd(state_handler=StateHandler(TestGitFlowHelper.DIR_PATH_TEST))

        branches: List[str] = []
        tags: List[str] = ['0.1.0']

        for b in branches:
            git.delete_branch_from_name(b, remote=True)

        for t in tags:
            git.delete_tag(t, remote=True)

        TestGitFlowHelper.clean_remote_repo()
        TestGitFlowHelper.clean_workdir()
