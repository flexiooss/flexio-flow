#! /usr/bin/env python3.7
from typing import Tuple, List, Optional, Dict
import getopt
import re
import sys
import os
from FlexioFlow.FlexioFlow import FlexioFlow
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.FlowAction import FlowAction
from Branches.Branches import Branches
from Exceptions.FileExistError import FileExistError


def parse_options(argv: List[str]) -> Tuple[List[str], Dict[str, str]]:
    options: Dict[str, str] = {}

    try:
        opts, args = getopt.gnu_getopt(argv, "hp:", ["help", "path"])
    except getopt.GetoptError:
        print('OUPS !!!')
        print('flexio-flow -h')
        print('May help you !!!!')
        sys.exit(2)

    for opt, arg in opts:
        arg = re.sub('[\s+]', '', arg)
        if opt in ("-h", "--help"):
            file = open(os.path.dirname(os.path.abspath(__file__)) + '/help.txt', 'r')
            print(file.read())
            sys.exit()
        if opt in ("-p", "--path"):
            options.update({'path': arg})

    return args, options


def extract_subject_action(argv: List[str]) -> Tuple[Optional[Branches], FlowAction]:
    branch: Optional[Branches] = None
    action: FlowAction

    arg: str
    for arg in argv:
        arg = re.sub('[\s+]', '', arg).lower()

        if FlowAction.has_value(arg):
            action = FlowAction(arg)
        elif Branches.has_value(arg):
            branch = Branches(arg)

    return branch, action


def command_orders(argv: List[str]) -> Tuple[FlowAction, Optional[Branches], Dict[str, str], str]:
    argv_no_options: List[str]
    options: Dict[str, str]
    argv_no_options, options = parse_options(argv)

    branch: Optional[Branches]
    action: FlowAction
    branch, action = extract_subject_action(argv_no_options)

    dir_path: str = options.get('path', os.getcwd())

    return action, branch, options, dir_path


def main(argv) -> None:
    action: FlowAction
    branch: Optional[Branches]
    options: Dict[str, str]
    dir_path: str
    action, branch, options, dir_path = command_orders(argv)

    FlexioFlow(
        action=action,
        branch=branch,
        options=options,
        dir_path=dir_path
    ).process()
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
