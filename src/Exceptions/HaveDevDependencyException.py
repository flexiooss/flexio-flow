from Schemes.Dependencies import Dependencies


class ReleasePlanException(Exception):
    def __init__(self, dependencies: Dependencies, message: str = ''):
        self.dependencies: Dependencies = dependencies
        self.message: str = message

    def __str__(self):
        return """
You should release before : 
{0!s}
{1!s}
""".format(self.dependencies, self.message)
