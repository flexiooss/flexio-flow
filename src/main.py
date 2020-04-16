#! /usr/bin/env python3.7
from ConsoleColors.PrintColor import PrintColor
from typing import Tuple, List, Optional, Dict, Union
import getopt
import re
import sys
import os

from ConsoleColors.Fg import Fg
from Core.ConfigHandler import ConfigHandler
from Core.Core import Core
from Exceptions.GitMergeConflictError import GitMergeConflictError
from FlexioFlow.Actions.IssueActions import IssueActions
from FlexioFlow.Actions.TopicActions import TopicActions
from FlexioFlow.FlexioFlow import FlexioFlow
from Branches.Actions.Actions import Actions
from Core.Actions.Actions import Actions as ActionsCore
from FlexioFlow.StateHandler import StateHandler
from PoomCiDependency.Actions.Actions import Actions as PoomCiActions
from FlexioFlow.Subject import Subject
from Schemes.Schemes import Schemes
from Branches.Branches import Branches
from VersionControl.VersionController import VersionController
from pathlib import Path

from VersionControlProvider.Flexio.FlexioRequestApiError import FlexioRequestApiError
from VersionControlProvider.Github.GithubRequestApiError import GithubRequestApiError


def clean_space(txt: str) -> str:
    return re.sub('[\s+]', '', txt)


def parse_options(argv: List[str]) -> Tuple[List[str], Dict[str, Union[str, Schemes, bool]]]:
    options: Dict[str, Union[str, Schemes, bool]] = {
        "debug": False
    }

    try:
        opts, args = getopt.gnu_getopt(argv, "HV:S:s:rcMNKF:D",
                                       ["help", "version-dir=", "scheme=", "scheme-dir=", "create", "read", "major",
                                        'no-cli', 'keep-branch', "repository-id=", "repository-name=",
                                        "repository-checkout-spec=", "filename=", "version=", "from=", "to=", "default",
                                        "message=", "debug"])
    except getopt.GetoptError:
        print(sys.argv[1:])
        print('OUPS !!!')
        print('try flexio-flow -H')
        sys.exit(2)

    for opt, arg in opts:

        if opt in ("-H", "--help"):
            file = open(os.path.dirname(os.path.abspath(__file__)) + '/help.txt', 'r')
            print(file.read())
            sys.exit()

        if opt in ("-V", "--version-dir"):
            options.update({'version-dir': arg})

        if opt in ("-s", "--scheme-dir"):
            options.update({'scheme-dir': arg})
        if opt in ("-S", "--scheme"):
            options.update({'scheme': Schemes[arg.upper()]})

        if opt in ("-r", "--read"):
            options.update({'read': True})
        if opt in ("-c", "--create"):
            options.update({'create': True})

        if opt in ("-M", "--major"):
            options.update({'major': True})
        if opt in ("-N", "--no-cli"):
            options.update({'no-cli': True})

        if opt in ("-K", "--keep-branch"):
            options.update({'keep-branch': True})

        if opt in ("-D", "--default"):
            options.update({'default': True})

        if opt in ("--repository-id"):
            options.update({'repository_id': clean_space(arg)})
        if opt in ("--repository-name"):
            options.update({'repository_name': clean_space(arg)})
        if opt in ("--repository-checkout-spec"):
            options.update({'repository_checkout_spec': clean_space(arg)})

        if opt in ("--filename", "-F"):
            options.update({'filename': clean_space(arg)})

        if opt in ("--version"):
            options.update({'version': clean_space(arg)})

        if opt in ("--debug"):
            options.update({'debug': True})

        if opt in ("--from"):
            options.update({'from': clean_space(arg)})

        if opt in ("--to"):
            options.update({'to': clean_space(arg)})

        if opt in ("--message"):
            options.update({'message': arg})

    return args, options


def extract_subject_action(argv: List[str]) -> Tuple[
    Optional[Branches], Optional[Actions], Optional[Subject], Optional[ActionsCore], Optional[IssueActions], Optional[
        TopicActions], Optional[
        PoomCiActions]]:
    branch: Optional[Branches] = None
    branch_action: Optional[Actions] = None
    subject: Optional[Subject] = None
    core_actions: Optional[ActionsCore] = None
    issue_action: Optional[IssueActions] = None
    topic_action: Optional[TopicActions] = None
    poom_ci_actions: Optional[PoomCiActions] = None

    arg: str
    for arg in argv:
        arg = re.sub('[\s+]', '', arg).lower()

        if Actions.has_value(arg):
            branch_action = Actions[arg.upper()]
        if Branches.has_value(arg):
            branch = Branches[arg.upper().replace('-', '_')]
        if Subject.has_value(arg):
            subject = Subject[arg.upper().replace('-', '_')]
        if ActionsCore.has_value(arg):
            core_actions = ActionsCore[arg.upper().replace('-', '_')]
        if IssueActions.has_value(arg) or TopicActions.has_value(arg):
            issue_action = IssueActions[arg.upper().replace('-', '_')]
        if TopicActions.has_value(arg):
            topic_action = TopicActions[arg.upper().replace('-', '_')]
        if PoomCiActions.has_value(arg):
            poom_ci_actions = PoomCiActions[arg.upper().replace('-', '_')]

    return branch, branch_action, subject, core_actions, issue_action, topic_action, poom_ci_actions


def command_orders(argv: List[str]) -> Tuple[
    Optional[Actions], Optional[Branches], Optional[Subject], Optional[ActionsCore], Dict[
        str, Union[str, Schemes, bool]], Path, Optional[IssueActions], Optional[TopicActions], Optional[
        PoomCiActions]]:
    argv_no_options: List[str]
    options: Dict[str, Union[str, Schemes, bool]]
    argv_no_options, options = parse_options(argv)

    branch: Optional[Branches]
    branch_action: Optional[Actions]
    subject: Optional[Subject]
    core_actions: Optional[ActionsCore]
    poom_ci_actions: Optional[PoomCiActions]

    branch, branch_action, subject, core_actions, issue_action, topic_action, poom_ci_actions = extract_subject_action(
        argv_no_options)

    version_dir: Path
    if options.get('version-dir'):
        version_dir = Path(str(options.get('version-dir')))
    else:
        file_dir: Optional[Path] = StateHandler.find_file_version(Path.cwd())
        if file_dir is not None:
            version_dir = file_dir
        else:
            version_dir = Path.cwd()

    return branch_action, branch, subject, core_actions, options, version_dir, issue_action, topic_action, poom_ci_actions


def main(argv) -> None:
    branch_action: Optional[Actions]
    branch: Optional[Branches]
    subject: Optional[Subject]
    core_action: Optional[ActionsCore]
    options: Dict[str, Union[str, Schemes, bool]]
    version_dir: Path
    issue_action: Optional[IssueActions]
    topic_action: Optional[TopicActions]

    branch_action, branch, subject, core_action, options, version_dir, issue_action, topic_action, poom_ci_actions = command_orders(
        argv)

    config_handler: ConfigHandler = ConfigHandler(Core.CONFIG_DIR)

    subject = Subject.BRANCH if subject is None else subject

    executor: FlexioFlow = FlexioFlow(subject=subject).set_environment(
        version_controller=VersionController.GIT,
        branch_action=branch_action,
        core_action=core_action,
        issue_action=issue_action,
        topic_action=topic_action,
        poom_ci_actions=poom_ci_actions,
        branch=branch,
        options=options,
        dir_path=version_dir,
        config_handler=config_handler
    )

    if options.get("debug"):
        executor.process()
    else:
        try:
            executor.process()
        except KeyboardInterrupt:
            PrintColor.log(Fg.FOCUS.value +"\n\n"+ '###  Flex bye bye budy !  ###' +"\n")
        except (
                FileNotFoundError, FileExistsError, ImportError, AttributeError, ValueError, KeyError,
                NotImplementedError,
                GitMergeConflictError, NotADirectoryError, TypeError, IndexError, GithubRequestApiError,
                ConnectionError,
                FlexioRequestApiError) as error:
            sys.stderr.write("""

{red}#######################################
# OUPS !!!
# {type}:{error}
#######################################{reset}

""".format(red=Fg.FAIL.value, type=error.__class__.__name__, error=error, reset=Fg.RESET.value))
            sys.stderr.write("Command terminated with wrong status code: 1" + "\n")
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
