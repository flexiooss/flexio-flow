class NoIssue(Exception):
    def __init__(self, message: str = ''):
        self.message: str = message

    def __str__(self):
        return """
No Issue for this branch
{0!s}
""".format(self.message)
