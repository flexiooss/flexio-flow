class TagVersionMismatch(Exception):
    def __init__(self, tag: str, state_version: str):
        self.tag: str = tag
        self.state_version: str = state_version

    def __str__(self):
        return """
Tag {0!s} holds a state file with version {1!s}.
The support version would be computed from a wrong base, check this tag.
""".format(self.tag, self.state_version)
