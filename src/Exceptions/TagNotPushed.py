class TagNotPushed(Exception):
    def __init__(self, tag: str):
        self.tag: str = tag

    def __str__(self):
        return """
Tag {0!s} exists locally but not on remote.
A support line must be reachable by everyone : git push origin {0!s}
""".format(self.tag)
