from __future__ import annotations
from typing import List
from FlexioFlow.Level import Level
from Log.Log import Log
from PoomCiDependency.Module import Module
from Schemes.Composer.ComposerFileHandler import ComposerFileHandler
from Schemes.Composer.PoomCiDependencies import PoomCiDependencies
from Schemes.Scheme import Scheme
from Schemes.Dependencies import Dependencies
from Schemes.Composer.PreCheck import PreCheck


class ComposerScheme(Scheme):
    DEV_SUFFIX: str = 'dev'

    def set_version(self) -> ComposerScheme:
        package_handler: ComposerFileHandler = ComposerFileHandler(self.state_handler.dir_path)
        package_handler.set_version(
            str(self.state_handler.state.version) if self.state_handler.state.level is Level.STABLE else '-'.join(
                [str(self.state_handler.state.version), self.DEV_SUFFIX])
        ).write()
        return self

    def release_precheck(self) -> Dependencies:
        comoser_handler: ComposerFileHandler = ComposerFileHandler(self.state_handler.dir_path)
        release_precheck: PreCheck = PreCheck(comoser_handler, self.DEV_SUFFIX)
        return release_precheck.process()

    def get_version(self) -> str:
        return '-'.join([self.state_handler.version_as_str(),
                         self.DEV_SUFFIX]) if self.state_handler.is_dev() else self.state_handler.version_as_str()

    def get_poom_ci_dependencies(self) -> List[Module]:
        return PoomCiDependencies(ComposerFileHandler(self.state_handler.dir_path)).process()

    def get_poom_ci_produces(self) -> List[Module]:
        package_handler: ComposerFileHandler = ComposerFileHandler(self.state_handler.dir_path)
        return [Module(package_handler.get_name(), self.get_version())]
