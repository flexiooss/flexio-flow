class NotCleanWorkingTree(Exception):
    def __init__(self, message: str = ''):
        self.message: str = message

    def __str__(self):
        return """
        
Your working tree is not clean
{0!s}
""".format(self.message)
