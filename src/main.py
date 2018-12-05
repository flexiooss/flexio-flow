#! /usr/bin/env python3
from typing import Tuple, List, Optional

import re
import sys
import os
from FlexioFlow.FlexioFlow import FlexioFlow
from utils.EnumUtils import EnumUtils
from FlexioFlow.FlexioFlowObjectHandler import FlexioFlowObjectHandler
from FlexioFlow.FlowAction import FlowAction
from Branches.Branches import Branches


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

def extract_subject_action(argv: List[str]) -> Tuple[Optional[Branches], FlowAction]:
    branch: Optional[Branches] = None
    action: FlowAction

    # print(argv)
    arg: str
    for arg in argv:
        arg = re.sub('[\s+]', '', arg).lower()
        # print(arg)
        # print(FlowAction[arg])
        # print(EnumUtils.has_value(FlowAction, arg))
        # print(EnumUtils.has_value(Branches, arg))
        if EnumUtils(FlowAction).has_value(arg):
            # print('FlowAction')
            # print(FlowAction(arg))
            action = FlowAction(arg)
        elif EnumUtils(Branches).has_value(arg):
            # print('Branches')
            # print(Branches(arg))
            branch = Branches(arg)

    return branch, action


def main(argv) -> None:
    ROOT_PATH: str = os.getcwd()
    print(ROOT_PATH)

    branch, action = extract_subject_action(argv)

    flow_object_handler: FlexioFlowObjectHandler = FlexioFlowObjectHandler(ROOT_PATH).load_file_config()
    print(str(flow_object_handler.state.version))

    FlexioFlow(
        action=action,
        branch=branch,
        flow_object_handler=flow_object_handler
    ).process()
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
