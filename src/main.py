#! /usr/bin/env python3.7
from typing import Tuple, List, Optional, Dict
import getopt
import re
import sys
import os

from Core.ConfigHandler import ConfigHandler
from Core.Core import Core
from FlexioFlow.FlexioFlow import FlexioFlow
from FlexioFlow.Actions.Actions import Actions
from Core.Actions.Actions import Actions as ActionsCore
from Schemes.Schemes import Schemes
from VersionControl.Branches import Branches
from VersionControl.VersionController import VersionController
from pathlib import Path


def parse_options(argv: List[str]) -> Tuple[List[str], Dict[str, str]]:
    options: Dict[str, str] = {}

    try:
        opts, args = getopt.gnu_getopt(argv, "hV:S:s:", ["help", "version-dir=", "scheme=", "scheme-dir="])
    except getopt.GetoptError:
        print('OUPS !!!')
        print('flexio-flow -h')
        print('May help you !!!!')
        sys.exit(2)
    print(opts)
    print(args)

    for opt, arg in opts:
        arg = re.sub('[\s+]', '', arg)
        if opt in ("-h", "--help"):
            file = open(os.path.dirname(os.path.abspath(__file__)) + '/help.txt', 'r')
            print(file.read())
            sys.exit()
        if opt in ("-V", "--version-dir"):
            options.update({'version-dir': arg})
        if opt in ("-s", "--scheme-dir"):
            options.update({'scheme-dir': arg})
        if opt in ("-S", "--scheme"):
            options.update({'scheme': Schemes[arg.upper()]})

    return args, options


def extract_subject_action(argv: List[str]) -> Tuple[
    Optional[Branches], Optional[Actions], bool, Optional[ActionsCore]]:
    branch: Optional[Branches] = None
    action: Optional[Actions] = None
    core: bool = False
    actions_core: Optional[ActionsCore] = None

    arg: str
    for arg in argv:
        arg = re.sub('[\s+]', '', arg).lower()

        if Actions.has_value(arg):
            action = Actions[arg.upper()]
        elif Branches.has_value(arg):
            branch = Branches[arg.upper()]
        elif arg == 'core':
            core = True
        elif ActionsCore.has_value(arg):
            actions_core = ActionsCore[arg.upper()]

    return branch, action, core, actions_core


def command_orders(argv: List[str]) -> Tuple[
    Optional[Actions], Optional[Branches], bool, Optional[ActionsCore], Dict[str, str], Path]:
    argv_no_options: List[str]
    options: Dict[str, str]
    argv_no_options, options = parse_options(argv)

    branch: Optional[Branches]
    action: Optional[Actions]
    core: bool
    actions_core: Optional[ActionsCore]

    branch, action, core, actions_core = extract_subject_action(argv_no_options)
    version_dir: Path = Path(options.get('version-dir')) if options.get('version-dir') else Path.cwd()
    print(options)

    print(version_dir)

    return action, branch, core, actions_core, options, version_dir


def main(argv) -> None:
    action: Optional[Actions]
    branch: Optional[Branches]
    core: bool
    actions_core: Optional[ActionsCore]
    options: Dict[str, str]
    dir_path: Path
    action, branch, core, actions_core, options, version_dir = command_orders(argv)

    config_handler: ConfigHandler = ConfigHandler(Core.CONFIG_DIR)

    if core:
        Core(actions_core, options=options, config_handler=config_handler).process()
    else:
        FlexioFlow(
            version_controller=VersionController.GITFLOW,
            action=action,
            branch=branch,
            options=options,
            dir_path=version_dir,
            config_handler=config_handler
        ).process()
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
