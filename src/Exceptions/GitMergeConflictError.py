from Branches.Branches import Branches


class GitMergeConflictError(Exception):
    def __init__(self, branch_name: str, message: str = ''):
        self.branch: str = branch_name
        self.message: str = message

    def __str__(self):
        return """
Conflict after merge : {0!s}
{1!s}
""".format(self.branch, self.message)
