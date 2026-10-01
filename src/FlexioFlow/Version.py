from __future__ import annotations
import re
from typing import Dict, Match, Optional


class Version:
    SEP: str = '.'
    DEFAULT_MAJOR: int = 1
    DEFAULT_MINOR: int = 0
    DEFAULT_PATCH: int = 0

    def __init__(self, major: int, minor: int, patch: int, support: Optional[int] = None) -> None:
        self.__major: int = major
        self.__minor: int = minor
        self.__patch: int = patch
        self.__support: Optional[int] = support

    @classmethod
    def from_str(cls, v: str) -> Version:
        matches: Match = cls.parse_str(v)
        support: Optional[str] = matches.groupdict().get('__support')

        return cls(
            major=int(matches.groupdict().get('__major', Version.DEFAULT_MAJOR)),
            minor=int(matches.groupdict().get('__minor', Version.DEFAULT_MINOR)),
            patch=int(matches.groupdict().get('__patch', Version.DEFAULT_PATCH)),
            support=int(support) if support is not None else None
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

    @property
    def support(self) -> Optional[int]:
        return self.__support

    @staticmethod
    def parse_str(v: str) -> Match:
        matches = re.match(
            r'^(?P<__major>\d+)\.(?P<__minor>\d+)\.(?P<__patch>\d+)(?:\.(?P<__support>\d+))?$', v)
        if not isinstance(matches, Match):
            raise ValueError(v + r'should be ^\d+\.\d+\.\d+(\.\d+)?$')
        return matches

    def next_major(self) -> Version:
        return Version(self.major + 1, 0, 0)

    def next_minor(self) -> Version:
        return Version(self.major, self.minor + 1, 0)

    def next_patch(self) -> Version:
        return Version(self.major, self.minor, self.patch + 1)

    def next_support(self) -> Version:
        return Version(self.major, self.minor, self.patch,
                       (self.support if self.support is not None else 0) + 1)

    def reset_patch(self) -> Version:
        return Version(self.major, self.minor, 0)

    def reset_minor(self) -> Version:
        return Version(self.major, 0, self.patch)

    def reset_major(self) -> Version:
        return Version(0, self.minor, self.patch)

    def to_dict(self) -> Dict[str, int]:
        values: Dict[str, int] = {
            'major': self.major,
            'minor': self.minor,
            'patch': self.patch
        }
        if self.support is not None:
            values['support'] = self.support
        return values

    def __str__(self):
        return str(
            self.SEP.join(
                list(
                    map(lambda x: str(x), self.to_dict().values())
                )
            )
        )
