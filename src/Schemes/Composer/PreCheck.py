from __future__ import annotations

from Schemes.Composer.ComposerFileHandler import ComposerFileHandler
from Schemes.Dependencies import Dependencies
from typing import Dict, Pattern, Match
import re


class PreCheck:

    def __init__(self, composer_handler: ComposerFileHandler, dev_suffix: str) -> None:
        self.__composer_handler: ComposerFileHandler = composer_handler
        self.__dev_suffix: str = dev_suffix

    def process(self) -> Dependencies:
        package_dependencies: Dict[str, str] = self.__composer_handler.data.get(ComposerFileHandler.DEPENDENCIES_KEY, {})
        dependencies: Dependencies = Dependencies()

        dep_id: str
        version: str
        for dep_id, version in package_dependencies.items():
            if self.is_flexio_dep(dep_id):
                if self.is_dev(version):
                    dependencies.append(dep_id, version)

        return dependencies

    def is_dev(self, version: str) -> bool:
        regexp: Pattern[str] = re.compile(
            '(?:(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?P<dev_suffix>-' + self.__dev_suffix + '))?$')
        return re.match(regexp, version) is not None

    def is_flexio_dep(self, name: str) -> bool:
        regexp: Pattern[str] = re.compile('^flexio(?:-(?:corp|oss))?/.*')
        return re.match(regexp, name) is not None
