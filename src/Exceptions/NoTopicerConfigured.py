class NoTopicerConfigured(Exception):
    def __init__(self, message: str = ''):
        self.message: str = message

    def __str__(self):
        return """
No Topicer configured
{0!s}
""".format(self.message)
