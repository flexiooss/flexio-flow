from __future__ import annotations
from Schemes.Dependencies import Dependencies
from typing import Dict, Pattern, Match
from Schemes.Package.PackageFileHandler import PackageFileHandler
import re


class PreCheck:

    def __init__(self, package_handler: PackageFileHandler, dev_suffix: str) -> None:
        self.__package_handler: PackageFileHandler = package_handler
        self.__dev_suffix: str = dev_suffix

    def process(self) -> Dependencies:
        package_dependencies: Dict[str, str] = self.__package_handler.data.get(PackageFileHandler.DEPENDENCIES_KEY, {})
        dependencies: Dependencies = Dependencies()
        print(package_dependencies)

        dep_id: str
        version: str
        for dep_id, version in package_dependencies.items():
            if self.is_dev(version):
                dependencies.append(dep_id, version)

        return dependencies

    def match_dev(self, v: str) -> Match:
        regexp: Pattern[str] = re.compile(
            '^(?:https|git).*(?P<is_git>\.git)+(?:#(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?P<is_dev>-' + self.__dev_suffix + ')?)?$')
        return re.match(regexp, v)

    def is_dev(self, version: str) -> bool:
        matches: Match = self.match_dev(version)
        return True if matches and matches.groupdict().get('is_git') and matches.groupdict().get('is_dev') else False
