class NoTagAtHead(Exception):
    def __str__(self):
        return """
HEAD is not on a version tag.
Checkout the production tag first, or pass --from-tag=<version>
"""
