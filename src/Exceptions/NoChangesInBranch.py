class NoChangesInBranch(Exception):
    def __init__(self, message: str = ''):
        self.message: str = message

    def __str__(self):
        return """
No changes in this branch : 
{0!s}
""".format(self.message)
