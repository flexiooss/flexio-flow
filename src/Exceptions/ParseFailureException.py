class ParseFailureException(Exception):
    def __init__(self, message: str = ''):
        self.message: str = message
