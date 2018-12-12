class NoBranchSelected(Exception):
    def __init__(self, message: str = ''):
        self.message: str = message

    def __str__(self):
        return """
No git Branch Selected
{0!s}
""".format(self.message)
