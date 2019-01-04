#! /usr/bin/env python3.7
from typing import Tuple, List, Optional, Dict, Union
import getopt
import re
import sys
import os

from Core.ConfigHandler import ConfigHandler
from Core.Core import Core
from FlexioFlow.Actions.Version import Version
from FlexioFlow.FlexioFlow import FlexioFlow
from Branches.Actions.Actions import Actions
from Core.Actions.Actions import Actions as ActionsCore
from FlexioFlow.StateHandler import StateHandler
from FlexioFlow.Subject import Subject
from Schemes.Schemes import Schemes
from Branches.Branches import Branches
from VersionControl.VersionController import VersionController
from pathlib import Path


def parse_options(argv: List[str]) -> Tuple[List[str], Dict[str, Union[str, Schemes]]]:
    options: Dict[str, Union[str, Schemes]] = {}

    try:
        opts, args = getopt.gnu_getopt(argv, "hV:S:s:", ["help", "version-dir=", "scheme=", "scheme-dir="])
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
        if opt in ("-V", "--version-dir"):
            options.update({'version-dir': arg})
        if opt in ("-s", "--scheme-dir"):
            options.update({'scheme-dir': arg})
        if opt in ("-S", "--scheme"):
            options.update({'scheme': Schemes[arg.upper()]})

    return args, options


def extract_subject_action(argv: List[str]) -> Tuple[
    Optional[Branches], Optional[Actions], Optional[Subject], Optional[ActionsCore]]:
    branch: Optional[Branches] = None
    branch_action: Optional[Actions] = None
    subject: Optional[Subject] = None
    core_actions: Optional[ActionsCore] = None

    arg: str
    for arg in argv:
        arg = re.sub('[\s+]', '', arg).lower()

        if Actions.has_value(arg):
            branch_action = Actions[arg.upper()]
        elif Branches.has_value(arg):
            branch = Branches[arg.upper()]
        elif Subject.has_value(arg):
            subject = Subject[arg.upper()]
        elif ActionsCore.has_value(arg):
            core_actions = ActionsCore[arg.upper()]

    return branch, branch_action, subject, core_actions


def command_orders(argv: List[str]) -> Tuple[
    Optional[Actions], Optional[Branches], Optional[Subject], Optional[ActionsCore], Dict[
        str, Union[str, Schemes]], Path]:
    argv_no_options: List[str]
    options: Dict[str, Union[str, Schemes]]
    argv_no_options, options = parse_options(argv)

    branch: Optional[Branches]
    branch_action: Optional[Actions]
    subject: Optional[Subject]
    core_actions: Optional[ActionsCore]

    branch, branch_action, subject, core_actions = extract_subject_action(argv_no_options)
    version_dir: Path = Path(str(options.get('version-dir'))) if options.get('version-dir') else Path.cwd()

    return branch_action, branch, subject, core_actions, options, version_dir


def main(argv) -> None:
    branch_action: Optional[Actions]
    branch: Optional[Branches]
    subject: Optional[Subject]
    core_actions: Optional[ActionsCore]
    options: Dict[str, Union[str, Schemes]]
    version_dir: Path
    branch_action, branch, subject, core_actions, options, version_dir = command_orders(argv)

    config_handler: ConfigHandler = ConfigHandler(Core.CONFIG_DIR)

    if subject is Subject.CORE:
        if core_actions is None:
            raise ValueError('should have Action')
        Core(core_actions, options=options, config_handler=config_handler).process()
    elif subject is Subject.VERSION:
        Version(StateHandler(version_dir).load_file_config(), options).process()
    else:
        if branch_action is None:
            raise ValueError('should have Action')
        FlexioFlow(
            version_controller=VersionController.GITFLOW,
            action=branch_action,
            branch=branch,
            options=options,
            dir_path=version_dir,
            config_handler=config_handler
        ).process()
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
