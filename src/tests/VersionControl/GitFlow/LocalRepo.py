from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import List


class LocalRepo:
    ENV: dict = {
        'GIT_AUTHOR_NAME': 'test',
        'GIT_AUTHOR_EMAIL': 'test@test',
        'GIT_COMMITTER_NAME': 'test',
        'GIT_COMMITTER_EMAIL': 'test@test',
        'PATH': '/usr/bin:/bin:/usr/local/bin',
        'HOME': '/tmp'
    }

    @classmethod
    def run(cls, path: Path, args: List[str]) -> str:
        completed = subprocess.run(
            args, cwd=path.as_posix(), env=cls.ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return completed.stdout.decode('utf-8').strip()

    @classmethod
    def clean(cls, path: Path) -> None:
        shutil.rmtree(path.as_posix(), True)

    @classmethod
    def create(cls, path: Path, version: str = '1.29.0') -> Path:
        cls.clean(path)
        path.mkdir(parents=True)
        cls.run(path, ['git', 'init', '-q', '-b', 'master'])
        (path / 'flexio-flow.yml').write_text(
            'level: stable\nschemes: []\ntopics: []\nversion: ' + version + '\n')
        (path / 'f.txt').write_text('l1\nl2\nl3\nl4\nl5\n')
        cls.run(path, ['git', 'add', '.'])
        cls.run(path, ['git', 'commit', '-qm', 'base'])
        cls.run(path, ['git', 'tag', '-a', version, '-m', version])
        cls.run(path, ['git', 'checkout', '-qb', 'develop'])
        cls.run(path, ['git', 'checkout', '-q', 'master'])
        return path

    @classmethod
    def with_remote(cls, path: Path) -> Path:
        remote: Path = Path(path.as_posix() + '_remote.git')
        cls.clean(remote)
        remote.mkdir(parents=True)
        cls.run(remote, ['git', 'init', '-q', '--bare'])
        cls.run(path, ['git', 'remote', 'add', 'origin', remote.as_posix()])
        cls.run(path, ['git', 'push', '-q', '--all', 'origin'])
        cls.run(path, ['git', 'push', '-q', '--tags', 'origin'])
        return remote
