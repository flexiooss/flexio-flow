import unittest
from typing import Dict, Optional

from requests import Response

from Core.ConfigHandler import ConfigHandler
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
from VersionControlProvider.Github.Github import Github
from VersionControlProvider.Github.GithubRequestApiError import GithubRequestApiError
from VersionControlProvider.Github.Ressources.IssueGithub import IssueGithub
from tests.VersionControl.GitFlow.TestGitFlowHelper import TestGitFlowHelper

INIT_VERSION: str = '0.0.0'
ISSUE_NUMBER: int = 14


class TestGitFlowHotfix(unittest.TestCase):
    state_handler: StateHandler
    git: GitCmd
    git_flow: GitFlowCmd
    config_handler: ConfigHandler
    github: Github

    def __hotfix_start(self, issue: Optional[IssueGithub] = None):
        if issue is not None:
            Git(self.state_handler).build_branch(Branches.HOTFIX).with_issue(issue).with_action(
                Actions.START).process()
        else:
            Git(self.state_handler).build_branch(Branches.HOTFIX).with_action(Actions.START).process()

    def __hotfix_finish(self, issue: Optional[IssueGithub] = None):
        if issue is not None:
            Git(self.state_handler).build_branch(Branches.HOTFIX).with_issue(issue).with_action(
                Actions.FINISH).process()
        else:
            Git(self.state_handler).build_branch(Branches.HOTFIX).with_action(Actions.FINISH).process()

    def __get_master_state(self) -> State:
        self.git.checkout(Branches.MASTER)
        return self.state_handler.state

    def __get_hotfix_state(self) -> State:
        self.git.checkout(Branches.HOTFIX)
        return self.state_handler.state

    def __get_dev_state(self) -> State:
        self.git.checkout(Branches.DEVELOP)
        return self.state_handler.state

    def __post_issue(self, issue: IssueGithub) -> IssueGithub:
        r: Response = self.github.create_issue(issue)

        if r.status_code is 201:
            issue_created: Dict[str, str] = r.json()
            return issue.with_number(int(issue_created.get('number')))
        else:
            raise GithubRequestApiError(r)

    def tearDown(self):
        TestGitFlowHelper.clean_workdir()
        TestGitFlowHelper.init_repo(INIT_VERSION)
        self.git.delete_branch_from_name(
            'hotfix/0.0.1-dev',
            remote=True
        ).delete_tag('0.0.1', remote=True).delete_branch_from_name(
            'hotfix/0.0.1-dev' + IssueGithub().with_number(ISSUE_NUMBER).get_ref(),
            remote=True
        )

        TestGitFlowHelper.clean_remote_repo()
        TestGitFlowHelper.clean_workdir()

    def setUp(self):
        # TestGitFlowHelper.clean_workdir()
        # TestGitFlowHelper.init_repo(INIT_VERSION)
        # GitCmd(state_handler=StateHandler(TestGitFlowHelper.DIR_PATH_TEST)).delete_branch_from_name(
        #     'hotfix/0.0.1-dev',
        #     remote=True
        # ).delete_tag('0.0.1', remote=True)

        # TestGitFlowHelper.clean_remote_repo()
        # TestGitFlowHelper.clean_workdir()

        self.state_handler = TestGitFlowHelper.init_repo(INIT_VERSION)

        self.git: GitCmd = GitCmd(state_handler=self.state_handler)
        self.git_flow: GitFlowCmd = GitFlowCmd(state_handler=self.state_handler)

    def __setup_config(self):
        self.config_handler = TestGitFlowHelper.setup_config_handler()
        self.github = TestGitFlowHelper.setup_github_repo(self.config_handler)

    def test_should_start_hotfix(self):
        self.assertIs(self.git.remote_branch_exists('hotfix/0.0.1-dev'), False)
        self.assertIs(self.git.local_branch_exists('hotfix/0.0.1-dev'), False)

        self.__hotfix_start()

        self.assertIs(self.git.local_branch_exists('hotfix/0.0.1-dev'), True)
        self.assertIs(self.git.remote_branch_exists('hotfix/0.0.1-dev'), True)

        state_master: State = self.__get_master_state()
        self.assertEqual(
            '0.0.0',
            str(state_master.version)
        )
        self.assertEqual(
            Level.STABLE,
            state_master.level
        )

        state_hotfix: State = self.__get_hotfix_state()
        self.assertEqual(
            '0.0.1',
            str(state_hotfix.version)
        )
        self.assertEqual(
            Level.DEV,
            state_hotfix.level
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
        with self.assertRaises(BranchAlreadyExist):
            self.__hotfix_start()

    def test_should_start_hotfix_with_issue(self):
        issue_created: IssueGithub = IssueGithub().with_number(ISSUE_NUMBER)

        self.assertIs(self.git.remote_branch_exists('hotfix/0.0.1-dev' + issue_created.get_ref()),
                      False)
        self.assertIs(self.git.local_branch_exists('hotfix/0.0.1-dev' + issue_created.get_ref()),
                      False)

        self.__hotfix_start(issue_created)

        self.assertIs(self.git.remote_branch_exists('hotfix/0.0.1-dev' + issue_created.get_ref()), True)
        self.assertIs(self.git.local_branch_exists('hotfix/0.0.1-dev' + issue_created.get_ref()),
                      True)

        state_master: State = self.__get_master_state()
        self.assertEqual(
            '0.0.0',
            str(state_master.version)
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

        state_hotfix: State = self.__get_hotfix_state()
        self.assertEqual(
            '0.0.1',
            str(state_hotfix.version)
        )
        self.assertEqual(
            Level.DEV,
            state_hotfix.level
        )
        with self.assertRaises(BranchAlreadyExist):
            self.__hotfix_start()

    def test_should_finish_hotfix(self):
        with self.assertRaises(BranchNotExist):
            self.__hotfix_finish()

        self.__hotfix_start()
        self.__hotfix_finish()

        state_master: State = self.__get_master_state()
        self.assertEqual(
            '0.0.1',
            str(state_master.version)
        )
        self.assertEqual(
            Level.STABLE,
            state_master.level
        )
        self.assertIs(self.git.remote_branch_exists('hotfix/0.0.1-dev'), False)

        self.assertIs(self.git.tag_exists('0.0.1', remote=False), True, 'Tag local should be 0.0.1')
        self.assertIs(self.git.tag_exists('0.0.1', remote=True), True, 'Tag remote should be 0.0.1')

        state_dev: State = self.__get_dev_state()
        self.assertEqual(
            '0.1.0',
            str(state_dev.version)
        )
        self.assertEqual(
            Level.DEV,
            state_dev.level
        )

    def test_should_finish_hotfix_with_issue(self):
        issue_created: IssueGithub = IssueGithub().with_number(ISSUE_NUMBER)

        with self.assertRaises(BranchNotExist):
            self.__hotfix_finish(issue_created)

        self.__hotfix_start(issue_created)
        self.__hotfix_finish(issue_created)

        state_master: State = self.__get_master_state()
        self.assertEqual(
            '0.0.1',
            str(state_master.version)
        )
        self.assertEqual(
            Level.STABLE,
            state_master.level
        )
        self.assertIs(
            self.git.remote_branch_exists('hotfix/0.0.1-dev' + issue_created.get_ref()),
            False
        )

        self.assertIs(self.git.tag_exists('0.0.1', remote=False), True, 'Tag local should be 0.0.1')
        self.assertIs(self.git.tag_exists('0.0.1', remote=True), True, 'Tag remote should be 0.0.1')

        state_dev: State = self.__get_dev_state()
        self.assertEqual(
            '0.1.0',
            str(state_dev.version)
        )
        self.assertEqual(
            Level.DEV,
            state_dev.level
        )

    def test_clean_fail(self):
        # TestGitFlowHelper.init_repo(INIT_VERSION)
        # GitCmd(state_handler=StateHandler(TestGitFlowHelper.DIR_PATH_TEST)).delete_branch_from_name(
        #     'hotfix/0.0.2-dev',
        #     remote=True
        # ).delete_tag('0.1.0', remote=True)

        TestGitFlowHelper.clean_remote_repo()
        TestGitFlowHelper.clean_workdir()
