from typing import List


class TagNotFound(Exception):
    def __init__(self, tag: str, known_tags: List[str]):
        self.tag: str = tag
        self.known_tags: List[str] = known_tags

    def __str__(self):
        return """
Tag not found locally nor on remote : {0!s}
Known tags : {1!s}
""".format(self.tag, ', '.join(self.known_tags))
