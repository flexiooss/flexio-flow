from __future__ import annotations

from subprocess import Popen

from FlexioFlow.StateHandler import StateHandler
from Schemes.Maven.ReportFileReader import ReportFileReader
from Schemes.Dependencies import Dependencies

import random
import string
import os


class MavenPreCheck:
    __state_handler: StateHandler

    def __init__(self, state_handler: StateHandler):
        self.__state_handler: StateHandler = state_handler

    def check(self) -> Dependencies:
        deps: Dependencies

        reportpath: str = '/tmp/' + ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

        status = Popen(
            ['mvn', 'clean', 'io.flexio.maven:flexio-flow-maven-plugin:1.0.0-SNAPSHOT:check-parent', '--fail-at-end', #'-e', '-X',
             '-Dreport.to=' + reportpath],
            cwd=self.__state_handler.dir_path.as_posix()
        ).wait()

        if status is 0:
            status = Popen(
                ['mvn', 'clean', 'io.flexio.maven:flexio-flow-maven-plugin:1.0.0-SNAPSHOT:check-deps', '--fail-at-end', #'-e', '-X',
                 '-Dreport.to=' + reportpath],
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
