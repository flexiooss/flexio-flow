from __future__ import annotations
from FlexioFlow.Actions.Action import Action
from Schemes.Schemes import Schemes
from Schemes.SchemeFactory import SchemeFactory
from Schemes.Scheme import Scheme
from Schemes.Dependencies import Dependencies
from typing import Type
from Exceptions.HaveDevDependencyException import HaveDevDependencyException


class PreCheck(Action):
    def process(self):
        scheme: Schemes
        for scheme in self.state_handler.state.schemes:
            sc: Type[Scheme] = SchemeFactory.create(scheme, self.state_handler)
            dev_dependencies: Dependencies = sc.release_precheck()
            if len(dev_dependencies):
                raise HaveDevDependencyException(dev_dependencies)
            print(dev_dependencies.__dict__())
