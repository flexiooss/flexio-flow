class NoFeatureName(ValueError):
    def __init__(self, message: str = ''):
        self.message: str = message

    def __str__(self):
        return """
No name for this feature branch
{0!s}
""".format(self.message)
