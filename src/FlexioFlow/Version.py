from __future__ import annotations
import re
from re import Match
from typing import Dict
from FlexioFlow.FlexioFlowValueObject import FlexioFlowValueObject


class Version:
    SEP: str = '.'

    def __init__(self, major: int, minor: int, patch: int) -> None:
        self.major: int = major
        self.minor: int = minor
        self.patch: int = patch

    @classmethod
    def from_str(cls, v: str) -> 'Version':
        matches: Match = cls.parse_str(v)

        return cls(
            major=int(matches.groupdict().get('major')),
            minor=int(matches.groupdict().get('minor')),
            patch=int(matches.groupdict().get('patch'))
        )

    @classmethod
    def from_flexio_flow(cls, v: FlexioFlowValueObject) -> 'Version':
        return cls.from_str(v.version)

    @staticmethod
    def parse_str(v: str) -> Match:
        return re.match('^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$', v)

    def next_major(self) -> 'Version':
        self.major += 1
        return self

    def next_minor(self) -> 'Version':
        self.minor += 1
        return self

    def next_patch(self) -> 'Version':
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
