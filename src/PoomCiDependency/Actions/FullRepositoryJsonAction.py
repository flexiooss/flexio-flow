from __future__ import annotations

from typing import Dict, Union, Optional

from FlexioFlow.StateHandler import StateHandler
from PoomCiDependency.Actions.FullRepositoryBuilder import FullRepositoryBuilder
from PoomCiDependency.FullRepository import FullRepository
from PoomCiDependency.PoomCiDependencyJSONEncoder import PoomCiDependencyJSONEncoder
from PoomCiDependency.Repository import Repository
from Schemes.Schemes import Schemes


class FullRepositoryJsonAction:
    repository: Optional[Repository] = None

    def __init__(self, state_handler: StateHandler, options: Dict[str, Union[str, Schemes, bool]]):
        self.state_handler: StateHandler = state_handler
        self.options: Dict[str, Union[str, Schemes, bool]] = options

    def process(self):
        full_repository: FullRepository = FullRepositoryBuilder(self.state_handler, self.options).build()
        print(PoomCiDependencyJSONEncoder().encode(full_repository))
