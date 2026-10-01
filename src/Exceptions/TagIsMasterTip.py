class TagIsMasterTip(Exception):
    def __init__(self, tag: str):
        self.tag: str = tag

    def __str__(self):
        return """
Tag {0!s} is the tip of master, nothing diverges.
Use hotfix start instead, it gives a three component version.
""".format(self.tag)
