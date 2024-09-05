from ConsoleColors.Fg import Fg
from VersionControlProvider.Github.Ressources.IssueGithub import IssueGithub
from VersionControlProvider.Topic import Topic


class CommonIssue:
    @staticmethod
    def issuer_message():
        print(
            r"""###############################################
################ {yellow}GITHUB ISSUER{reset} ################
###############################################
""".format(yellow=Fg.NOTICE.value, reset=Fg.RESET.value))

    @staticmethod
    def print_resume_issue(issue: IssueGithub):
        print(
            r"""###############################################
########### {green}    Issue {number!s}    {reset}############
###############################################{green}
title : {title!s}
number : {number!s}
url : {url!s}{reset}
###############################################
""".format(
                green=Fg.NOTICE.value,
                title=issue.title,
                number=issue.number,
                url=issue.url,
                reset=Fg.RESET.value
            )
        )
