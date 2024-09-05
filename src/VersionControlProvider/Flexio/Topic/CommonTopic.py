from ConsoleColors.Fg import Fg
from VersionControlProvider.Topic import Topic


class CommonTopic:
    @staticmethod
    def print_resume_topic(topic: Topic):
        print(
            r"""###############################################
################# {green}Topic {number!s}{reset} #################
###############################################{green}
title : {title!s}
number : {number!s}
url : {url!s}{reset}
###############################################
""".format(
                green=Fg.NOTICE.value,
                title=topic.title,
                number=topic.number,
                url=topic.url(),
                reset=Fg.RESET.value
            )
        )
