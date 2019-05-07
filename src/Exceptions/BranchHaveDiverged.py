class BranchHaveDiverged(Exception):
    def __init__(self, message: str = ''):
        self.message: str = message

    def __str__(self):
        return """
Your branch has diverged : 
{0!s}
""".format(self.message)
