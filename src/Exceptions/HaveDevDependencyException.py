from Schemes.Dependencies import Dependencies


class HaveDevDependencyException(Exception):
    def __init__(self, dependencies: Dependencies, message: str = ''):
        self.dependencies: Dependencies = dependencies
        self.message: str = message

    def __str__(self):
        return """
You should release before : 
{0!s}
{1!s}
""".format(self.dependencies.__dict__(), self.message)
