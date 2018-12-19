import unittest
import time
from pathlib import Path

from requests import Response

from Core.Config import Config
from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Github.ConfigGithub import ConfigGithub
from VersionControlProvider.Github.Github import Github
from VersionControlProvider.Github.Repo import Repo
from VersionControlProvider.Issue import Issue

TOKEN_TEST: str = 'daca8bdd8c905bbae9637b6d2e98b1a3ea238747'
USER: str = 'TomAchT'
CONFIG_DIR: Path = Path('/tmp/')


class TestGithub(unittest.TestCase):

    def setUp(self):
        self.config_handler = ConfigHandler(CONFIG_DIR)
        self.config_handler.config = Config(ConfigGithub(
            activate=True,
            user=USER,
            token=TOKEN_TEST
        ))

    def test_get_user(self):
        r: Response = Github(self.config_handler).get_user()
        self.assertIs(r.status_code, 200)

        falsy_config_handler = ConfigHandler(CONFIG_DIR)
        falsy_config_handler.config = Config(ConfigGithub(
            activate=True,
            user='dudu',
            token='dudu'
        ))
        r: Response = Github(falsy_config_handler).get_user()
        self.assertIsNot(r.status_code, 200)

    def test_list_labels(self):
        r: Response = Github(self.config_handler).with_repo(
            Repo(owner='flexiooss', repo='flexio-flow-punching-ball')).get_labels()
        self.assertIs(r.status_code, 200)
        print(r.json())

    def test_create_issue(self):
        issue: Issue = Issue()
        issue.title = 'issue test ' + str(int(time.time()))
        issue.body = 'test description'
        issue.assign(USER)
        issue.label('bug')

        r: Response = Github(self.config_handler).with_repo(
            Repo(owner='flexiooss', repo='flexio-flow-punching-ball')).create_issue(issue)
        print(r.status_code)
        print(r.content)
        print(r.json())
        self.assertIs(r.status_code, 201)

    def test_create_issue_comment(self):
        issue: Issue = Issue()
        issue.title = 'issue test ' + str(int(time.time()))
        issue.body = 'test description'
        issue.assign(USER)
        issue.label('bug')

        r: Response = Github(self.config_handler).with_repo(
            Repo(owner='flexiooss', repo='flexio-flow-punching-ball')).create_issue(issue)

        issue_created: Issue = Issue()
        issue_created.number = r.json().get('number')

        r: Response = Github(self.config_handler).with_repo(
            Repo(owner='flexiooss', repo='flexio-flow-punching-ball')).create_comment(issue_created,
                                                                                      body='super commentaire')
        print(r.status_code)
        print(r.content)
        print(r.json())
        self.assertIs(r.status_code, 201)
