from __future__ import annotations

from PoomCiDependency.Module import Module
from Schemes.Dependencies import Dependencies
from typing import Dict, Pattern, Match, List
from Schemes.Package.PackageFileHandler import PackageFileHandler
import re


class PoomCiDependencies:

    def __init__(self, package_handler: PackageFileHandler) -> None:
        self.__package_handler: PackageFileHandler = package_handler

    def process(self) -> List[Module]:
        package_dependencies: Dict[str, str] = self.__package_handler.data.get(PackageFileHandler.DEPENDENCIES_KEY, {})
        dependencies: List[Module] = []

        dep_id: str
        version: str
        for dep_id, version in package_dependencies.items():
            dependencies.append(Module(dep_id, version))

        return dependencies
