from __future__ import annotations

from VersionControlProvider.Flexio.FlexioRessource import FlexioRessource
from VersionControlProvider.Flexio.FlexioTopic import FlexioTopic
from VersionControlProvider.Github.Ressources.IssueGithub import IssueGithub
from VersionControlProvider.Issue import Issue


class FlexioIssue(Issue, FlexioRessource):
    RECORD_ID: str = '_id'
    RESOURCE_ID: str = '5c336d47f3bb2517583dac84'

    TOPIC_ID: str = '5c336d65f3bb251c3d227327'
    GITHUB_NUMBER_ID: str = '5c336de1f3bb251c3d227329'
    GITHUB_TITLE_ID: str = '5c336d4ff3bb2560bf1c964f'
    GITHUB_URL_ID: str = '5c336d5df3bb25217136750b'
    SLUG: str = 'issue'

    topic: FlexioTopic
    github_title: str
    github_number: int
    github_url: str

    def with_topic(self, topic: FlexioTopic) -> FlexioIssue:
        self.topic = topic
        return self

    def set_github_issue(self, issue: IssueGithub)-> FlexioIssue:
        self.github_number = issue.number
        self.github_title = issue.title
        self.github_url = issue.url
        return self

    def get_ref(self) -> str:
        if self.number is None:
            raise ValueError('Issue should have a number')
        return '{prefix!s}{number!s}'.format(prefix=self.PREFIX, number=self.number)

    def __dict__(self):
        ret: dict = {
            self.TOPIC_ID: self.topic.number,
            self.GITHUB_NUMBER_ID: self.github_number,
            self.GITHUB_TITLE_ID: self.github_title,
            self.GITHUB_URL_ID: self.github_url
        }
        if self.id is not None:
            ret[self.RECORD_ID] = self.id
        return ret

    @classmethod
    def build_from_api(cls, json: dict) -> FlexioIssue:
        issue: FlexioIssue = FlexioIssue()
        issue.id = json.get(cls.RECORD_ID)
        issue.github_number = json.get(cls.GITHUB_NUMBER_ID)
        issue.topic = FlexioTopic().with_id(json.get(cls.TOPIC_ID))
        issue.github_title = json.get(cls.GITHUB_TITLE_ID)
        issue.github_url = json.get(cls.GITHUB_URL_ID)
        return issue
