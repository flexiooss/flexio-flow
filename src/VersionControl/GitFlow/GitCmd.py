from __future__ import annotations
import re
from re import Match
from subprocess import Popen, PIPE
from typing import List, Optional, Pattern
from Exceptions.FileNotExistError import FileNotExistError
from Exceptions.NoBranchSelected import NoBranchSelected
from FlexioFlow.StateHandler import StateHandler
from VersionControl.BranchHandler import BranchHandler
from VersionControl.Branches import Branches
from VersionControl.GitFlow.GitConfig import GitConfig
from VersionControlProvider.Github.Repo import Repo


class GitCmd:
    def __init__(self, state_handler: StateHandler):
        self.__state_handler = state_handler
        self.__branch: Optional[Branches] = None
        self.__remote_branch_name: Optional[str] = None

    def __exec(self, args: List[str]):
        Popen(args, cwd=self.__state_handler.dir_path.as_posix()).communicate()

    def __exec_for_stdout(self, args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE, cwd=self.__state_handler.dir_path.as_posix()).communicate()
        return stdout.strip().decode('utf-8')

    def add_all(self) -> GitCmd:
        self.__exec(['git', 'add', '.'])
        return self

    def branch_exists(self, branch: Branches, remote: bool) -> bool:
        branch_name: str = self.get_branch_name_from_git(branch)
        return self.branch_exists_from_name(branch_name, remote)

    def branch_exists_from_name(self, branch: str, remote: bool) -> bool:
        if remote:
            resp: str = self.__exec_for_stdout(
                ['git', 'ls-remote', GitConfig.REMOTE.value, 'refs/heads/' + branch])
            return len(resp) > 0 and re.match(re.compile('.*refs/heads/' + branch + '$'), resp) is not None
        else:
            resp: str = self.__get_branch_name_from_git_list(branch)
            return len(resp) > 0

    def checkout(self, branch: Branches) -> GitCmd:
        self.__branch = branch
        self.__ensure_remote_branch_name()
        self.checkout_with_branch_name(self.__remote_branch_name)
        return self

    def checkout_with_branch_name(self, branch: str):
        self.__exec(['git', 'checkout', branch])
        try:
            self.__state_handler.load_file_config()
        except FileNotExistError as e:
            print(e)
        return self

    def create_branch_from(self, target_branch_name: str, source: Branches) -> GitCmd:
        source_branch_name: str = self.get_branch_name_from_git(source)
        self.__exec(['git', 'checkout', '-b', target_branch_name, source_branch_name])
        try:
            self.__state_handler.load_file_config()
        except FileNotExistError as e:
            print(e)
        return self

    def __ensure_remote_branch_name(self) -> GitCmd:
        if not self.__branch:
            raise NoBranchSelected('Try with GitCmd.checkout(branch_name:str) before')
        branch_name: str = self.__branch.value
        if self.__branch in [Branches.HOTFIX]:
            self.__exec(['git', 'checkout', Branches.MASTER.value])
            self.__state_handler.load_file_config()
            branch_name: str = BranchHandler.branch_name_from_version(
                Branches.HOTFIX,
                self.__state_handler.state.version
            )
        if self.__branch in [Branches.RELEASE]:
            self.__exec(['git', 'checkout', Branches.DEVELOP.value])
            self.__state_handler.load_file_config()
            branch_name: str = BranchHandler.branch_name_from_version(
                Branches.RELEASE,
                self.__state_handler.state.version
            )
        self.__remote_branch_name = branch_name
        return self

    def commit(self, msg: str) -> GitCmd:
        self.__exec(["git", "commit", "-am", msg])
        return self

    def clone(self, url: str) -> GitCmd:
        self.__exec(['git', 'clone', url, '.'])
        return self

    def delete_tag(self, tag: str, remote: bool) -> GitCmd:
        if remote:
            self.__exec(['git', 'push', GitConfig.REMOTE.value, '--delete', tag])
        else:
            self.__exec(['git', 'tag', '-d', tag])
        return self

    def delete_branch(self, branch: Branches, remote: bool) -> GitCmd:
        branch_name: str = self.__get_branch_name_from_git_list(branch.value)
        return self.delete_branch_from_name(branch_name, remote)

    def delete_branch_from_name(self, branch: str, remote: bool) -> GitCmd:
        if remote:
            self.__exec(['git', 'push', GitConfig.REMOTE.value, '--delete', branch])
        else:
            self.__exec(['git', 'branch', '-d', branch])
        return self

    def get_branch_name_from_git(self, branch: Branches) -> str:
        branch_name: str = self.__get_branch_name_from_git_list(branch.value)
        return branch_name

    def __get_branch_name_from_git_list(self, branch: str) -> str:
        branch: str = self.__exec_for_stdout(['git', 'branch', '--list', '|', 'grep', branch + '*'])
        return re.sub(
            pattern=re.compile('^\*?\s*'),
            repl='',
            string=branch
        )

    def get_conflict(self) -> str:
        return self.__exec_for_stdout(['git', 'ls-files', '-u'])

    def get_repo(self) -> Repo:
        url: str = self.__exec_for_stdout(['git', 'config', '--get', 'remote.origin.url'])
        regexp: Pattern[str] = re.compile(
            '^git@github\.com:(?P<owner>[\w\d._-]*)/(?P<repo>[\w\d._-]*)\.git$',
            re.IGNORECASE)
        matches: Match = re.match(regexp, url)
        if matches is None:
            raise ValueError(
                'remote.origin.url not match with : ^git@github\.com:(?P<owner>[\w\d._-]*)/(?P<repo>[\w\d._-]*)\.git$')
        return Repo(owner=matches.groupdict().get('owner'), repo=matches.groupdict().get('repo'))

    def get_current_branch_name(self) -> str:
        return self.__exec_for_stdout(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])

    def has_conflict(self) -> bool:
        return len(self.get_conflict()) > 0

    def last_tag(self) -> str:
        return self.__exec_for_stdout(['git', 'describe', '--abbrev=0', '--tags'])

    def merge(self, branch: Branches, options: List[str] = []) -> GitCmd:
        target_branch_name: str = self.get_branch_name_from_git(branch)
        self.__exec(['git', 'merge', target_branch_name, *options])
        self.__state_handler.load_file_config()
        return self

    def merge_with_version_message(self, branch: Branches, options: List[str] = []) -> GitCmd:
        return self.merge(
            branch,
            options=['--commit', '-m', '"merge : ' + self.get_branch_name_from_git(branch) + '"',
                     *options])

    def merge_with_theirs(self, branch: Branches) -> GitCmd:
        target_branch_name: str = self.get_branch_name_from_git(branch)
        self.__exec(
            ['git', 'merge', target_branch_name, '-m', '"merge : ' + target_branch_name + '"', '--strategy-option',
             'theirs'])
        return self

    def push_tag(self, tag: str) -> GitCmd:
        self.__exec(["git", "push", GitConfig.REMOTE.value, tag])
        return self

    def pull(self) -> GitCmd:
        self.__exec(["git", "pull"])
        return self

    def push(self) -> GitCmd:
        self.__exec(["git", "push"])
        return self

    def push_force(self) -> GitCmd:
        if not self.__branch:
            raise NoBranchSelected('Try with GitCmd.checkout(branch_name:str) before')
        self.__exec(['git', 'push', '--force', GitConfig.REMOTE.value, self.get_current_branch_name()])
        return self

    def tag_exists(self, tag: str, remote: bool) -> bool:
        if remote:
            resp: str = self.__exec_for_stdout(['git', 'ls-remote', GitConfig.REMOTE.value, 'refs/tags/' + tag])
            return len(resp) > 0 and re.match(re.compile('.*refs/tags/' + tag + '$'), resp) is not None
        else:
            resp: str = self.__exec_for_stdout(['git', 'tag', '-l', '|', 'grep', tag])
            return len(resp) > 0 and re.match(re.compile('^' + tag + '$'), resp) is not None

    def reset_to_tag(self, tag: str) -> GitCmd:
        self.__exec(['git', 'reset', '--hard', tag])
        return self

    def set_upstream(self) -> GitCmd:
        if not self.__branch:
            raise NoBranchSelected('Try with GitCmd.checkout(branch_name:str) before')
        self.__exec(["git", "push", "--set-upstream", GitConfig.REMOTE.value, self.get_current_branch_name()])
        return self

    def tag(self, tag: str, msg: Optional[str] = None) -> GitCmd:
        msg = msg if msg else tag
        self.__exec(["git", "tag", "-a", tag, "-m", "'" + msg + "'"])
        return self
