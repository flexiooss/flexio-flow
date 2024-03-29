from Branches.Branches import Branches


class BranchAlreadyExist(Exception):
    def __init__(self, branch: str, message: str = ''):
        self.branch: str = branch
        self.message: str = message

    def __str__(self):
        return """
Git Branch Branch Already Exist : {0!s}
{1!s}
""".format(self.branch, self.message)
