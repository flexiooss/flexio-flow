from __future__ import annotations

from typing import Dict, Union, Type, Optional, List

from FlexioFlow.StateHandler import StateHandler
from PoomCiDependency.FullRepository import FullRepository
from PoomCiDependency.Module import Module
from PoomCiDependency.Repository import Repository
from Schemes.Scheme import Scheme
from Schemes.SchemeBuilder import SchemeBuilder
from Schemes.Schemes import Schemes


class FullRepositoryBuilder:
    repository: Optional[Repository] = None

    def __init__(self, state_handler: StateHandler, options: Dict[str, Union[str, Schemes, bool]]):
        self.state_handler: StateHandler = state_handler
        self.options: Dict[str, Union[str, Schemes, bool]] = options

    def __ensure_have_repo(self):

        repository_id: str = self.options.get('repository_id')
        repository_name = self.options.get('repository_name')
        repository_checkout_spec = self.options.get('repository_checkout_spec')

        if repository_id is None or repository_name is None or repository_checkout_spec is None:
            raise ValueError('Option missing, repository_id, repository_name, repository_checkout_spec')

        self.repository = Repository(id=repository_id, name=repository_name, checkout_spec=repository_checkout_spec)

    def __get_scheme_option_or_default(self) -> Schemes:
        schemes: Optional[Schemes] = self.options.get('scheme')
        if schemes is None:
            schemes = self.state_handler.first_scheme()
        if schemes is None:
            raise ValueError('No schemes given')
        return schemes

    def build(self) -> FullRepository:
        self.__ensure_have_repo()

        full_repository: FullRepository = FullRepository.from_repository(self.repository)

        scheme: Scheme = SchemeBuilder.create(self.__get_scheme_option_or_default(), self.state_handler)

        poom_ci_dependencies: Optional[List[Module]] = scheme.get_poom_ci_dependencies()
        if poom_ci_dependencies is not None:
            full_repository.dependencies = poom_ci_dependencies

        poom_ci_produces: Optional[List[Module]] = scheme.get_poom_ci_produces()
        if poom_ci_produces is not None:
            full_repository.produces = poom_ci_produces

        return full_repository
