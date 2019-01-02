from __future__ import annotations
import re
from typing import Dict, Match


class Version:
    SEP: str = '.'

    def __init__(self, major: int, minor: int, patch: int) -> None:
        self.__major: int = major
        self.__minor: int = minor
        self.__patch: int = patch

    @classmethod
    def from_str(cls, v: str) -> Version:
        matches: Match = cls.parse_str(v)

        return cls(
            major=int(matches.groupdict().get('__major', 0)),
            minor=int(matches.groupdict().get('__minor', 0)),
            patch=int(matches.groupdict().get('__patch', 0))
        )

    @property
    def major(self) -> int:
        return self.__major

    @property
    def minor(self) -> int:
        return self.__minor

    @property
    def patch(self) -> int:
        return self.__patch

    @staticmethod
    def parse_str(v: str) -> Match:
        matches = re.match('^(?P<__major>\d+)\.(?P<__minor>\d+)\.(?P<__patch>\d+)$', v)
        if not isinstance(matches, Match):
            raise ValueError(v + 'should be ^\d+\.\d+\.\d+$')
        return matches

    def next_major(self) -> Version:
        return Version(self.major + 1, self.minor, self.patch)

    def next_minor(self) -> Version:
        return Version(self.major, self.minor + 1, self.patch)

    def next_patch(self) -> Version:
        return Version(self.major, self.minor, self.patch + 1)

    def reset_patch(self) -> Version:
        return Version(self.major, self.minor, 0)

    def to_dict(self) -> Dict[str, int]:
        return {
            'major': self.major,
            'minor': self.minor,
            'patch': self.patch
        }

    def __str__(self):
        return str(
            self.SEP.join(
                list(
                    map(lambda x: str(x), self.to_dict().values())
                )
            )
        )
