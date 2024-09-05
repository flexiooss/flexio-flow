from __future__ import annotations

from PoomCiDependency.Module import Module
from Schemes.Dependencies import Dependencies
from typing import Dict, Pattern, Match, List, Optional
from Schemes.Package.PackageFileHandler import PackageFileHandler
import re


class PoomCiDependencies:

    def __init__(self, package_handler: PackageFileHandler) -> None:
        self.__package_handler: PackageFileHandler = package_handler

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
        package_dependencies: Dict[str, str] = self.__package_handler.data.get(PackageFileHandler.DEPENDENCIES_KEY, {})
        dependencies: List[Module] = []

        dep_id: str
        version: str
        for dep_id, version in package_dependencies.items():
            dependencies.append(Module(dep_id, self.__clean_version(version)))

        return dependencies
