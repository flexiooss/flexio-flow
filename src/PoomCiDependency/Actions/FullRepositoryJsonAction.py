from __future__ import annotations
from pathlib import Path

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

        if self.options.get('filename') is not None:
            filename: Path = Path(self.options.get('filename'))

            if filename.is_file():
                raise FileExistsError(filename)

            with filename.open('w') as outfile:
                outfile.write(PoomCiDependencyJSONEncoder().encode(full_repository))

        else:
            print(PoomCiDependencyJSONEncoder().encode(full_repository))
