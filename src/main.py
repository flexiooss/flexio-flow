#! /usr/bin/env python3.7
from typing import Tuple, List, Optional, Dict
import getopt
import re
import sys
import os
from FlexioFlow.FlexioFlow import FlexioFlow
from FlexioFlow.Actions.Actions import Actions
from VersionControl.Branches import Branches
from VersionControl.VersionController import VersionController
from pathlib import Path
import pprint


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


def extract_subject_action(argv: List[str]) -> Tuple[Optional[Branches], Actions]:
    branch: Optional[Branches] = None
    action: Actions

    arg: str
    for arg in argv:
        arg = re.sub('[\s+]', '', arg).lower()

        if Actions.has_value(arg):
            action = Actions(arg)
        elif Branches.has_value(arg):
            branch = Branches(arg)

    return branch, action


def command_orders(argv: List[str]) -> Tuple[Actions, Optional[Branches], Dict[str, str], Path]:
    argv_no_options: List[str]
    options: Dict[str, str]
    argv_no_options, options = parse_options(argv)

    branch: Optional[Branches]
    action: Actions
    branch, action = extract_subject_action(argv_no_options)
    dir_path: Path = Path(options.get('path')) if options.get('path') else Path.cwd()

    return action, branch, options, dir_path


def main(argv) -> None:
    action: Actions
    branch: Optional[Branches]
    options: Dict[str, str]
    dir_path: Path
    action, branch, options, dir_path = command_orders(argv)

    FlexioFlow(
        version_controller=VersionController.GITFLOW,
        action=action,
        branch=branch,
        options=options,
        dir_path=dir_path
    ).process()
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
