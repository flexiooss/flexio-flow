from __future__ import annotations

from VersionControl.Branch import Branch


class Master(Branch):

    def process(self):
        raise NotImplementedError
