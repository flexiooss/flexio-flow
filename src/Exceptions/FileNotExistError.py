from pathlib import Path

class FileNotExistError(Exception):
    def __init__(self, file_path: Path, message: str = ''):
        self.file_path: Path = file_path
        self.message: str = message

    def __str__(self):
        return """
File not exists at : {0!s}
{1!s}
""".format(self.file_path, self.message)