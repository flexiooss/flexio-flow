from __future__ import annotations
import re
from typing import Dict


class Version:
    SEP: str = '.'

    major: int = 0
    minor: int = 0
    patch: int = 0

    def __init__(self, major: int, minor: int, patch: int) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch

    @staticmethod
    def fromStr(v: str) -> 'Version':
        matches = re.match('^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$', v)
        return Version(
            major=int(matches.groupdict().get('major')),
            minor=int(matches.groupdict().get('minor')),
            patch=int(matches.groupdict().get('patch'))
        )

    def major(self) -> 'Version':
        self.major += 1
        return self

    def minor(self) -> 'Version':
        self.minor += 1
        return self

    def patch(self) -> 'Version':
        self.patch += 1
        return self

    def reset_patch(self) -> 'Version':
        self.patch = 0
        return self

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
