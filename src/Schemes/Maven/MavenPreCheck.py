from __future__ import annotations

from subprocess import Popen

from Schemes.Maven import ReportFileReader
from Schemes.Dependencies import Dependencies
from pathlib import Path

import random
import string
import os


class MavenPreCheck:
    dir_path: str

    def __init__(self, dir_path: Path):
        self.dir_path = dir_path

    def check(self) -> Dependencies:
        deps: Dependencies

        reportpath: str = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

        status = Popen(
            ['mvn', 'clean', 'io.flexio.maven:flexio-flow-maven-plugin:1.0.0-SNAPSHOT:check-deps', '--fail-at-end', '-Dreport.to=/tmp/' + reportpath],
            cwd=self.__state_handler.dir_path.as_posix()
        ).wait()

        if status is 0:
            deps = Dependencies()
        else:
            deps = ReportFileReader(reportpath).read()

        if os.path.exists(reportpath):
            os.remove(reportpath)
        else:
            pass

        return deps
