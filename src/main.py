#! /usr/bin/env python3
from typing import Dict, Tuple, List

import re
import os
import sys
import getopt
from pprint import pprint
from src.FlexioFlowValueObject import FlexioFlowValueObject
import os

SUBJECT = ("init", "hotfix", "release")
ACTION = ("start", "finish", "plan")


# def parse_options(argv: List[str]) -> Tuple[str, str]:
#     subject: str
#     action: str
#     pprint(argv)
#
#     try:
#         opts, args = getopt.getopt(argv, "ihrfs", ["help", "init", "hotfix", "release", "start", "finish", "plan"])
#     except getopt.GetoptError:
#         print('flexio-flow <init> | <hotfix start|finish> | <release start|plan|finish>')
#         sys.exit(2)
#
#     pprint(opts)
#     pprint(args)
#
#     for opt, arg in args:
#         arg = re.sub('[\s+]', '', arg)
#         print(arg)
#         print(opt)
#         # if opt in ("-h", "--help"):
#         #     print
#         #     'hotballoon-shed:ci:update_meta -i <package_file> -u <dependencies_url> -v <version> -d <docker_image>'
#         #     sys.exit()
#         # elif opt in ("-i", "--ifile"):
#         #     package_file = arg
#         # elif opt in ("-u", "--url"):
#         #     dependencies_url = arg
#         # elif opt in ("-v", "--version"):
#         #     version = arg
#         # elif opt in ("-d", "--docker_image"):
#         #     docker_image = arg
#
#     # return subject, action


def extract_subject_action(argv: List[str]) -> Tuple[str, str]:
    subject: str
    action: str

    arg: str
    for arg in argv:
        arg = re.sub('[\s+]', '', arg)
        if arg in ACTION:
            action = arg
        elif arg in SUBJECT:
            subject = arg

    return subject, action


def main(argv) -> None:
    subject, action = extract_subject_action(argv)

    print(os.getcwd())
    pprint((subject, action))


    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
