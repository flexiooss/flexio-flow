import unittest
from typing import Optional

from slugify import slugify

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
FEATURE_NAME: int = 'Ma super nouvelle feature accentué'


class TestGitFlowFeature(unittest.TestCase):
    state_handler: StateHandler

    def __feature_start(self, issue: Optional[IssueGithub] = None):
        if issue is not None:
            Git(self.state_handler).build_branch(Branches.FEATURE).with_issue(issue).with_action(
                Actions.START).with_name(FEATURE_NAME).process()
        else:
            Git(self.state_handler).build_branch(Branches.FEATURE).with_action(Actions.START).with_name(
                FEATURE_NAME).process()

    def __feature_finish(self, issue: Optional[IssueGithub] = None):
        if issue is not None:
            Git(self.state_handler).build_branch(Branches.FEATURE).with_issue(issue).with_action(
                Actions.FINISH).with_name(FEATURE_NAME).process()
        else:
            Git(self.state_handler).build_branch(Branches.FEATURE).with_action(Actions.FINISH).with_name(
                FEATURE_NAME).process()

    def __get_master_state(self) -> State:
        self.git.checkout(Branches.MASTER)
        return self.state_handler.state

    def __get_feature_state(self, branch_name: str) -> State:
        print('__get_feature_state')
        self.git.checkout_with_branch_name(branch_name)
        return self.state_handler.state

    def __get_dev_state(self) -> State:
        self.git.checkout(Branches.DEVELOP)
        return self.state_handler.state

    def tearDown(self):
        TestGitFlowHelper.clean_workdir()
        TestGitFlowHelper.init_repo(INIT_VERSION)

        self.git.delete_branch_from_name(
            'feature/' + slugify(FEATURE_NAME) + '-0.1.0-dev',
            True
        ).delete_branch_from_name(
            'feature/' + slugify(FEATURE_NAME) + '-0.1.0-dev' + IssueGithub().with_number(ISSUE_NUMBER).get_ref(),
            True
        ).delete_branch_from_name(
            'release/ma-super-nouvelle-feature-accentue-0.1.0-dev',
            True
        )

        TestGitFlowHelper.clean_remote_repo()
        TestGitFlowHelper.clean_workdir()

    def setUp(self):
        self.state_handler = TestGitFlowHelper.init_repo(INIT_VERSION)

        self.git: GitCmd = GitCmd(state_handler=self.state_handler)
        self.git_flow: GitFlowCmd = GitFlowCmd(state_handler=self.state_handler)

    def test_vide(self):
        pass

    def test_should_start_feature(self):
        self.assertIs(self.git.remote_branch_exists('feature/' + slugify(FEATURE_NAME) + '-0.1.0-dev'),
                      False)
        self.assertIs(self.git.local_branch_exists('feature/' + slugify(FEATURE_NAME) + '-0.1.0-dev'),
                      False)

        self.__feature_start()

        self.assertIs(self.git.local_branch_exists('feature/' + slugify(FEATURE_NAME) + '-0.1.0-dev'),
                      True)
        self.assertIs(self.git.remote_branch_exists('feature/' + slugify(FEATURE_NAME) + '-0.1.0-dev'),
                      True)

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

        state_feature: State = self.__get_feature_state('feature/' + slugify(FEATURE_NAME) + '-0.1.0-dev')
        self.assertEqual(
            '0.1.0',
            str(state_feature.version)
        )
        self.assertEqual(
            Level.DEV,
            state_feature.level
        )
        with self.assertRaises(BranchAlreadyExist):
            self.__feature_start()

    def test_should_start_feature_with_issue(self):
        issue_created: IssueGithub = IssueGithub().with_number(ISSUE_NUMBER)

        self.assertIs(self.git.remote_branch_exists(
            'feature/' + slugify(FEATURE_NAME) + '-0.1.0-dev' + IssueGithub().with_number(ISSUE_NUMBER).get_ref()),
            False)
        self.assertIs(self.git.local_branch_exists(
            'feature/' + slugify(FEATURE_NAME) + '-0.1.0-dev' + IssueGithub().with_number(ISSUE_NUMBER).get_ref()),
            False)

        self.__feature_start(issue_created)

        self.assertIs(self.git.remote_branch_exists(
            'feature/' + slugify(FEATURE_NAME) + '-0.1.0-dev' + IssueGithub().with_number(ISSUE_NUMBER).get_ref()),
            True)
        self.assertIs(self.git.local_branch_exists(
            'feature/' + slugify(FEATURE_NAME) + '-0.1.0-dev' + IssueGithub().with_number(ISSUE_NUMBER).get_ref()),
            True)

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

        state_feature: State = self.__get_feature_state(
            'feature/' + slugify(FEATURE_NAME) + '-0.1.0-dev' + IssueGithub().with_number(ISSUE_NUMBER).get_ref())
        self.assertEqual(
            '0.1.0',
            str(state_feature.version)
        )
        self.assertEqual(
            Level.DEV,
            state_feature.level
        )
        with self.assertRaises(BranchAlreadyExist):
            self.__feature_start(issue_created)

    def test_should_finish_feature(self):
        with self.assertRaises(BranchNotExist):
            self.__feature_finish()

        self.__feature_start()
        self.__feature_finish()

        state_master: State = self.__get_master_state()
        self.assertEqual(
            '0.0.0',
            str(state_master.version)
        )
        self.assertEqual(
            Level.STABLE,
            state_master.level
        )
        self.assertFalse(
            self.git.remote_branch_exists('feature/' + slugify(FEATURE_NAME) + '-0.1.0-dev'))

        state_dev: State = self.__get_dev_state()
        self.assertEqual(
            '0.1.0',
            str(state_dev.version)
        )
        self.assertEqual(
            Level.DEV,
            state_dev.level
        )

    def test_should_finish_release_with_issue(self):
        issue_created: IssueGithub = IssueGithub().with_number(ISSUE_NUMBER)

        with self.assertRaises(BranchNotExist):
            self.__feature_finish()

        self.__feature_start(issue_created)
        self.__feature_finish(issue_created)

        self.__feature_start()
        self.__feature_finish()

        state_master: State = self.__get_master_state()
        self.assertEqual(
            '0.0.0',
            str(state_master.version)
        )
        self.assertEqual(
            Level.STABLE,
            state_master.level
        )
        self.assertFalse(
            self.git.remote_branch_exists(
                'feature/' + slugify(FEATURE_NAME) + '-0.1.0-dev' + IssueGithub().with_number(ISSUE_NUMBER).get_ref())

        state_dev: State = self.__get_dev_state()

        self.assertEqual(
            '0.1.0',
            str(state_dev.version)
        )
        self.assertEqual(
            Level.DEV,
            state_dev.level
        )
