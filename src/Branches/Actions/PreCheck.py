from __future__ import annotations
from Branches.Actions.Action import Action
from Log.Log import Log
from Schemes.Schemes import Schemes
from Schemes.SchemeBuilder import SchemeBuilder
from Schemes.Scheme import Scheme
from Schemes.Dependencies import Dependencies
from typing import Type
from Exceptions.HaveDevDependencyException import HaveDevDependencyException


class PreCheck(Action):
    def process(self):
        Log.info('Start unstable version precheck')

        scheme: Schemes
        for scheme in self.state_handler.state.schemes:
            Log.info('Precheck for : ' + scheme.value)
            sc: Scheme = SchemeBuilder.create(scheme, self.state_handler)
            dev_dependencies: Dependencies = sc.release_precheck()
            print(dev_dependencies.__dict__())
            if len(dev_dependencies):
                raise HaveDevDependencyException(dev_dependencies)
