class RemoteDivergence(Exception):
    def __init__(self, message: str = ''):
        self.message: str = message

    def __str__(self):
        return """
Your local branch has diverged from remote : 
{0!s}
""".format(self.message)
