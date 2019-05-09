from __future__ import annotations

from typing import List

from PoomCiDependency.Module import Module
from PoomCiDependency.Repository import Repository


class FullRepository:
    id: str
    name: str
    checkoutSpec: str
    dependencies: List[Module] = []
    produces: List[Module] = []

    def __init__(self, id: str, name: str, checkout_spec: str):
        self.id = id
        self.name = name
        self.checkout_spec = checkout_spec
        self.dependencies = []
        self.produces = []

    @staticmethod
    def from_repository(repository: Repository) -> FullRepository:
        return FullRepository(repository.id, repository.name, repository.checkout_spec)

    def append_dependency(self, dependency: Module) -> FullRepository:
        self.dependencies.append(dependency)
        return self

    def append_produce(self, produce: Module) -> FullRepository:
        self.produces.append(produce)
        return self