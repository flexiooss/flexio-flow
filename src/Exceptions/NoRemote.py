class NoRemote(Exception):
    def __init__(self, message: str = ''):
        self.message: str = message

    def __str__(self):
        return """
No Remote configured for this repo : 
{0!s}
""".format(self.message)
