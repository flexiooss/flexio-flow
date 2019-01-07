import unittest
from typing import Optional

from Exceptions.BranchAlreadyExist import BranchAlreadyExist
from Exceptions.BranchNotExist import BranchNotExist
from Branches.Actions.Actions import Actions
from FlexioFlow.State import State
from FlexioFlow.Level import Level
from FlexioFlow.StateHandler import StateHandler
from VersionControl.Git.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.Git.GitCmd import GitCmd
from Branches.Branches import Branches
from VersionControl.Git.Git import Git
from VersionControlProvider.Github.Ressources.IssueGithub import IssueGithub
from tests.VersionControl.GitFlow.TestGitFlowHelper import TestGitFlowHelper

INIT_VERSION: str = '0.0.0'
ISSUE_NUMBER: int = 14


class TestGitFlowRelease(unittest.TestCase):
    state_handler: StateHandler

    def __release_start(self, issue: Optional[IssueGithub] = None):
        if issue is not None:
            Git(self.state_handler).build_branch(Branches.RELEASE).with_issue(issue).with_action(
                Actions.START).process()
        else:
            Git(self.state_handler).build_branch(Branches.RELEASE).with_action(Actions.START).process()

    def __release_finish(self, issue: Optional[IssueGithub] = None):
        if issue is not None:
            Git(self.state_handler).build_branch(Branches.RELEASE).with_issue(issue).with_action(
                Actions.FINISH).process()
        else:
            Git(self.state_handler).build_branch(Branches.RELEASE).with_action(Actions.FINISH).process()

    def __get_master_state(self) -> State:
        self.git.checkout(Branches.MASTER)
        return self.state_handler.state

    def __get_release_state(self) -> State:
        print('__get_feature_state')
        self.git.checkout(Branches.RELEASE)
        return self.state_handler.state

    def __get_dev_state(self) -> State:
        self.git.checkout(Branches.DEVELOP)
        return self.state_handler.state

    def tearDown(self):
        TestGitFlowHelper.clean_workdir()
        TestGitFlowHelper.init_repo(INIT_VERSION)

        self.git.delete_branch_from_name(
            'release/0.1.0',
            True
        ).delete_branch_from_name(
            'release/0.1.0' + IssueGithub().with_number(ISSUE_NUMBER).get_ref(),
            True
        ).delete_tag('0.2.0', remote=True)

        TestGitFlowHelper.clean_remote_repo()
        TestGitFlowHelper.clean_workdir()

    def setUp(self):
        self.state_handler = TestGitFlowHelper.init_repo(INIT_VERSION)

        self.git: GitCmd = GitCmd(state_handler=self.state_handler)
        self.git_flow: GitFlowCmd = GitFlowCmd(state_handler=self.state_handler)

    def test_vide(self):
        pass

    def test_should_start_release(self):
        self.assertIs(self.git.branch_exists_from_name('release/0.1.0', remote=True), False)
        self.assertIs(self.git.branch_exists_from_name('release/0.1.0', remote=False), False)

        self.__release_start()

        self.assertIs(self.git.branch_exists_from_name('release/0.1.0', remote=False), True)
        self.assertIs(self.git.branch_exists_from_name('release/0.1.0', remote=True), True)

        state_master: State = self.__get_master_state()
        self.assertEqual(
            '0.0.0',
            INIT_VERSION
        )
        self.assertEqual(
            Level.STABLE,
            state_master.level
        )

        state_dev: State = self.__get_dev_state()
        self.assertEqual(
            '0.1.0',
            str(state_dev.version)
        )
        self.assertEqual(
            Level.DEV,
            state_dev.level
        )

        state_release: State = self.__get_release_state()
        self.assertEqual(
            '0.1.0',
            str(state_release.version)
        )
        self.assertEqual(
            Level.STABLE,
            state_release.level
        )
        with self.assertRaises(BranchAlreadyExist):
            self.__release_start()

    def test_should_start_release_with_issue(self):
        issue_created: IssueGithub = IssueGithub().with_number(ISSUE_NUMBER)

        self.assertIs(
            self.git.branch_exists_from_name('release/0.1.0' + IssueGithub().with_number(ISSUE_NUMBER).get_ref(),
                                             remote=True), False)
        self.assertIs(
            self.git.branch_exists_from_name('release/0.1.0' + IssueGithub().with_number(ISSUE_NUMBER).get_ref(),
                                             remote=False), False)

        self.__release_start(issue_created)

        self.assertIs(
            self.git.branch_exists_from_name('release/0.1.0' + IssueGithub().with_number(ISSUE_NUMBER).get_ref(),
                                             remote=False), True)
        self.assertIs(
            self.git.branch_exists_from_name('release/0.1.0' + IssueGithub().with_number(ISSUE_NUMBER).get_ref(),
                                             remote=True), True)

        state_master: State = self.__get_master_state()
        self.assertEqual(
            '0.0.0',
            INIT_VERSION
        )
        self.assertEqual(
            Level.STABLE,
            state_master.level
        )

        state_dev: State = self.__get_dev_state()
        self.assertEqual(
            '0.1.0',
            str(state_dev.version)
        )
        self.assertEqual(
            Level.DEV,
            state_dev.level
        )

        state_release: State = self.__get_release_state()
        self.assertEqual(
            '0.1.0',
            str(state_release.version)
        )
        self.assertEqual(
            Level.STABLE,
            state_release.level
        )
        with self.assertRaises(BranchAlreadyExist):
            self.__release_start()

    def test_should_finish_release(self):
        with self.assertRaises(BranchNotExist):
            self.__release_finish()

        self.__release_start()
        self.__release_finish()

        state_master: State = self.__get_master_state()
        self.assertEqual(
            '0.1.0',
            str(state_master.version)
        )
        self.assertEqual(
            Level.STABLE,
            state_master.level
        )
        self.assertIs(self.git.branch_exists_from_name('release/0.1.0', remote=True), False)

        self.assertIs(self.git.tag_exists('0.1.0', remote=False), True, 'Tag local should be 0.1.0')
        self.assertIs(self.git.tag_exists('0.1.0', remote=True), True, 'Tag remote should be 0.1.0')

        state_dev: State = self.__get_dev_state()
        self.assertEqual(
            '0.2.0',
            str(state_dev.version)
        )
        self.assertEqual(
            Level.DEV,
            state_dev.level
        )

    def test_should_finish_release_with_issue(self):
        issue_created: IssueGithub = IssueGithub().with_number(ISSUE_NUMBER)
        with self.assertRaises(BranchNotExist):
            self.__release_finish()

        self.__release_start(issue_created)
        self.__release_finish(issue_created)

        state_master: State = self.__get_master_state()
        self.assertEqual(
            '0.1.0',
            str(state_master.version)
        )
        self.assertEqual(
            Level.STABLE,
            state_master.level
        )
        self.assertIs(
            self.git.branch_exists_from_name('release/0.1.0' + IssueGithub().with_number(ISSUE_NUMBER).get_ref(),
                                             remote=True), False)

        self.assertIs(self.git.tag_exists('0.1.0', remote=False), True, 'Tag local should be 0.1.0')
        self.assertIs(self.git.tag_exists('0.1.0', remote=True), True, 'Tag remote should be 0.1.0')

        state_dev: State = self.__get_dev_state()
        self.assertEqual(
            '0.2.0',
            str(state_dev.version)
        )
        self.assertEqual(
            Level.DEV,
            state_dev.level
        )
