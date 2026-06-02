from __future__ import annotations

from typing import List

from FlexioFlow.Level import Level
from PoomCiDependency.Module import Module
from Schemes.ClaudePlugin.ClaudePluginFileHandler import ClaudePluginFileHandler
from Schemes.Dependencies import Dependencies
from Schemes.Scheme import Scheme


class ClaudePluginScheme(Scheme):
    DEV_SUFFIX: str = 'dev'
    PACKAGE_FILE: str = 'package.json'
    PLUGIN_FILE: str = '.claude-plugin/plugin.json'

    def __version_str(self) -> str:
        base = str(self.state_handler.state.version)
        if self.state_handler.state.level is Level.STABLE:
            return base
        return '-'.join([base, self.DEV_SUFFIX])

    def set_version(self) -> ClaudePluginScheme:
        version_str = self.__version_str()
        ClaudePluginFileHandler(
            self.state_handler.dir_path / self.PACKAGE_FILE
        ).set_version(version_str).write()
        ClaudePluginFileHandler(
            self.state_handler.dir_path / self.PLUGIN_FILE
        ).set_version(version_str).write()
        return self

    def release_precheck(self) -> Dependencies:
        return Dependencies()

    def get_version(self) -> str:
        return self.__version_str()

    def get_poom_ci_dependencies(self) -> List[Module]:
        return []

    def get_poom_ci_produces(self) -> List[Module]:
        handler = ClaudePluginFileHandler(self.state_handler.dir_path / self.PACKAGE_FILE)
        return [Module(handler.get_name(), self.get_version())]
