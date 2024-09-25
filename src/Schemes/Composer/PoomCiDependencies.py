from __future__ import annotations

from PoomCiDependency.Module import Module
from Schemes.Composer.ComposerFileHandler import ComposerFileHandler
from Schemes.Dependencies import Dependencies
from typing import Dict, Pattern, Match, List, Optional
import re


class PoomCiDependencies:

    def __init__(self, composer_handler: ComposerFileHandler) -> None:
        self.__composer_handler: ComposerFileHandler = composer_handler

    def __is_git(self, v: str) -> bool:
        regexp: Pattern[str] = re.compile(
            '^(?:https|git).*\.git.*')
        return re.search(regexp, v) is not None

    def __git_version(self, v: str) -> str:
        regexp: Pattern[str] = re.compile(
            '^(?:https|git).*\.git(?:#(?P<version>.*))?$')
        return re.match(regexp, v).groupdict().get('version')

    def __clean_version(self, version: str) -> Optional[str]:
        if self.__is_git(version):
            version = self.__git_version(version)

        if version is None:
            return version

        regexp: Pattern[str] = re.compile(r'^[\^~=>]')
        version = re.sub(regexp, '', version)

        return version

    def process(self) -> List[Module]:
        composer_dependencies: Dict[str, str] = self.__composer_handler.data.get(ComposerFileHandler.DEPENDENCIES_KEY,
                                                                                 {})
        dependencies: List[Module] = []

        dep_id: str
        version: str
        for dep_id, version in composer_dependencies.items():
            dependencies.append(Module(dep_id, self.__clean_version(version)))

        return dependencies
