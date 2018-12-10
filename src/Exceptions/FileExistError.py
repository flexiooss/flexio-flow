from pathlib import Path

class FileExistError(Exception):
    def __init__(self, file_path: Path, message: str = ''):
        self.file_path: str = file_path
        self.message: str = message

    def __str__(self):
        return """
File exists : {0!s}
{1!s}
""".format(self.file_path, self.message)
