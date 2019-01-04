class NoIssuerConfigured(Exception):
    def __init__(self, message: str = ''):
        self.message: str = message

    def __str__(self):
        return """
No git Issuer configured
{0!s}
""".format(self.message)
