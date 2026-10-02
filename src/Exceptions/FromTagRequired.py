class FromTagRequired(Exception):
    def __str__(self):
        return """
support-branch start requires --from-tag=<version>

A support line always starts from an explicit production tag.
Being checked out somewhere is never taken as an answer.
"""
