from __future__ import annotations
from typing import Dict, Optional
import requests
from requests import Response
from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Github.Repo import Repo
from VersionControlProvider.Github.Ressources.IssueGithub import IssueGithub
from VersionControlProvider.Github.Ressources.Milestone import Milestone


class Github:
    BASE_URL: str = 'https://api.github.com'

    def __init__(self, config_handler: ConfigHandler):
        self.config_handler: ConfigHandler = config_handler
        self.repo: Optional[Repo] = None

    def with_repo(self, repo: Repo) -> Github:
        self.repo = repo
        return self

    def __auth(self, headers: Dict[str, str]) -> Dict[str, str]:
        if self.config_handler.config.github.token:
            headers['Authorization'] = 'token {github_token!s}'.format(
                github_token=self.config_handler.config.github.token)
        else:
            raise AttributeError('No user or token')
        return headers

    def __repo_base_url(self) -> str:
        if self.repo is None:
            raise ValueError('repo should be set')
        return '/'.join([self.BASE_URL, 'repos', *self.repo.to_list()])

    def __orgs_base_url(self) -> str:
        if self.repo is None:
            raise ValueError('repo should be set')
        return '/'.join([self.BASE_URL, 'orgs', self.repo.owner])

    def get_users(self) -> Response:
        url: str = '/'.join([self.__orgs_base_url(), 'members'])
        headers: Dict[str, str] = {}
        return requests.get(url, headers=self.__auth(headers))

    def get_user(self) -> Response:
        url: str = '/'.join([self.BASE_URL, 'user'])
        headers: Dict[str, str] = {}
        return requests.get(url, headers=self.__auth(headers))

    def create_issue(self, issue: IssueGithub) -> Response:
        url: str = '/'.join([self.__repo_base_url(), 'issues'])
        return requests.post(url, json=issue.__dict__(), headers=self.__auth({}))

    def read_issue(self, issue: IssueGithub) -> Response:
        url: str = '/'.join([self.__repo_base_url(), 'issues', str(issue.number)])
        r: Response = requests.get(url, headers=self.__auth({}))
        if r.status_code == 200:
            return r
        else:
            raise FileNotFoundError

    def create_milestone(self, milestone: Milestone) -> Response:
        url: str = '/'.join([self.__repo_base_url(), 'milestones'])
        return requests.post(url, json=milestone.__dict__(), headers=self.__auth({}))

    def get_labels(self) -> Response:
        url: str = '/'.join([self.__repo_base_url(), 'labels'])
        return requests.get(url, headers=self.__auth({}))

    def get_open_milestones(self) -> Response:
        url: str = '/'.join([self.__repo_base_url(), 'milestones'])
        return requests.get(url, headers=self.__auth({}))

    def create_comment(self, issue: IssueGithub, body: str) -> Response:
        url: str = '/'.join([self.__repo_base_url(), 'issues', str(issue.number), 'comments'])
        return requests.post(url, json={'body': body}, headers=self.__auth({}))
