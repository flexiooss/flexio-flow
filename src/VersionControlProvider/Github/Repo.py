from typing import List


class Repo:
    def __init__(self, owner: str, repo: str):
        self.owner: str = owner
        self.repo: str = repo

    def to_list(self) -> List[str]:
        return [self.owner, self.repo]
