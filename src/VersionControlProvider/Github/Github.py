from __future__ import annotations
from typing import Dict, Optional
import requests
from requests import Response
from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Github.Repo import Repo
from VersionControlProvider.Issue import Issue


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

    def get_user(self) -> Response:
        url: str = '/'.join([self.BASE_URL, 'user'])
        headers: Dict[str, str] = {}
        r: Response = requests.get(url, headers=self.__auth(headers))
        print(r.status_code)
        print(r.json())
        return r

    def create_issue(self, issue: Issue) -> Response:
        url: str = '/'.join([self.__repo_base_url(), 'issues'])
        return requests.post(url, json=issue.__dict__(), headers=self.__auth({}))

    def get_labels(self) -> Response:
        url: str = '/'.join([self.__repo_base_url(), 'labels'])
        return requests.get(url, headers=self.__auth({}))

    def create_comment(self, issue: Issue, body: str) -> Response:
        url: str = '/'.join([self.__repo_base_url(), 'issues', issue.number, 'comments'])
        return requests.post(url, json={'body': body}, headers=self.__auth({}))
