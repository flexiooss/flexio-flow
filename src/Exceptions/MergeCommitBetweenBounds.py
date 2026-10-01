class MergeCommitBetweenBounds(Exception):
    def __init__(self, branch: str):
        self.branch: str = branch

    def __str__(self):
        return """
A merge commit stands between the bounds of {0!s}.
The squashed diff would carry more than the fixes.
Finish with --no-merge and report to develop by hand.
""".format(self.branch)
