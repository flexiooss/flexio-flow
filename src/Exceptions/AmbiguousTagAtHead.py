from typing import List


class AmbiguousTagAtHead(Exception):
    def __init__(self, tags: List[str]):
        self.tags: List[str] = tags

    def __str__(self):
        return """
Several version tags point at HEAD : {0!s}
Pass --from-tag=<version> to choose
""".format(', '.join(self.tags))
