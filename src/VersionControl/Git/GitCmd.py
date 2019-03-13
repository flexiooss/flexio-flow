from __future__ import annotations
import re
from pathlib import Path
from subprocess import Popen, PIPE
from typing import List, Optional, Pattern, Match

from Exceptions.BranchNotExist import BranchNotExist
from FlexioFlow.StateHandler import StateHandler
from Branches.Branches import Branches
from VersionControl.Git.GitConfig import GitConfig
from VersionControlProvider.Github.Repo import Repo


class GitCmd:
    SPACES_PATTERN: Pattern = re.compile('^\*?\s*')

    def __init__(self, state_handler: StateHandler):
        self.__state_handler = state_handler

    def __exec(self, args: List[str]) -> Popen:
        child: Popen = Popen(args, cwd=self.__state_handler.dir_path.as_posix())
        child.communicate()
        return child

    def __exec_for_stdout(self, args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE, cwd=self.__state_handler.dir_path.as_posix()).communicate()
        return self.__decode_stdout(stdout)

    def __decode_stdout(self, stdout) -> str:
        return stdout.strip().decode('utf-8')

    def add_all(self) -> GitCmd:
        self.__exec(['git', 'add', '.'])
        return self

    def branch_exists_from_branches(self, branch: Branches) -> bool:
        return self.local_branch_exists_from_branches(branch) or self.remote_branch_exists_from_branches(branch)

    def local_branch_exists_from_branches(self, branch: Branches) -> bool:
        branch_name: str = self.get_branch_name_from_git(branch)
        return self.local_branch_exists(branch_name)

    def remote_branch_exists_from_branches(self, branch: Branches) -> bool:
        branch_name: str = self.get_branch_name_from_git(branch)
        return self.remote_branch_exists(branch_name)

    def branch_exists(self, branch: str) -> bool:
        return self.local_branch_exists(branch) or self.remote_branch_exists(branch)

    def local_branch_exists(self, branch: str) -> bool:
        resp: str = self.__get_branch_name_from_git_list(branch)
        print(resp)
        return len(resp) > 0

    def remote_branch_exists(self, branch: str) -> bool:
        resp: str = self.__exec_for_stdout(
            ['git', 'ls-remote', GitConfig.REMOTE.value, 'refs/heads/' + branch])
        return len(resp) > 0 and re.match(re.compile('.*refs/heads/' + branch + '$'), resp) is not None

    def can_commit(self) -> bool:
        stdout: str = self.__exec_for_stdout(['git', 'status', '-s'])
        return stdout is not None and len(stdout) > 0

    def checkout(self, branch: Branches, options: List[str] = []) -> GitCmd:
        self.checkout_with_branch_name(self.get_branch_name_from_git(branch), options).reload_state()
        return self

    def checkout_without_refresh_state(self, branch: Branches, options: List[str] = []) -> GitCmd:
        self.checkout_with_branch_name(self.get_branch_name_from_git(branch), options)
        return self

    def checkout_with_branch_name(self, branch: str, options: List[str] = []) -> GitCmd:
        print('branch')
        print(branch)
        self.__exec(['git', 'checkout', branch, *options])
        return self

    def reload_state(self) -> GitCmd:
        try:
            self.__state_handler.load_file_config()
        except FileNotFoundError as e:
            print(e)
        return self

    def checkout_file_with_branch_name(self, branch: str, file: Path) -> GitCmd:
        if not file.is_file():
            raise FileNotFoundError()
        self.__exec(['git', 'checkout', branch, file.as_posix()])

        return self

    def create_branch_from(self, target_branch_name: str, source: Branches) -> GitCmd:
        source_branch_name: str = self.get_branch_name_from_git(source)
        self.__exec(['git', 'checkout', '-b', target_branch_name, source_branch_name])
        try:
            self.__state_handler.load_file_config()
        except FileNotFoundError as e:
            print(e)
        return self

    def commit(self, msg: str, options: List[str] = []) -> GitCmd:
        self.__exec(["git", "commit", "-am", msg, *options])
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
        if branch in [Branches.MASTER, Branches.DEVELOP]:
            return branch.value
        branch_name: str = self.__get_branch_name_from_git_list(branch.value)
        return branch_name

    def __get_branch_name_from_git_list(self, branch: str) -> str:
        p1 = Popen(
            ['git', 'branch', '--list'],
            stdout=PIPE,
            cwd=self.__state_handler.dir_path.as_posix()
        )

        p2 = Popen(
            ['grep', '-E', r"^\*?\s*.*{branch}.*".format(branch=branch)],
            stdin=p1.stdout,
            stdout=PIPE,
            cwd=self.__state_handler.dir_path.as_posix())
        p1.stdout.close()
        result = p2.communicate()[0]
        p1.wait()

        branch_name = self.__decode_stdout(result)
        return re.sub(
            pattern=self.SPACES_PATTERN,
            repl='',
            string=branch_name
        )

    def get_conflict(self) -> str:
        return self.__exec_for_stdout(['git', 'ls-files', '-u'])

    def get_branches(self) -> List[str]:
        return self.get_local_branches() + self.get_remote_branches()

    def get_local_branches(self) -> List[str]:
        return self.__exec_for_stdout(['git', 'for-each-ref', '--sort', 'refname', '--format="%(refname:short)"',
                                       self.local_branch_name()]).splitlines()

    def get_remote_branches(self) -> List[str]:
        return self.__exec_for_stdout(['git', 'for-each-ref', '--sort', 'refname', '--format="%(refname:short)"',
                                       self.remote_branch_name()]).splitlines()

    def get_repo(self) -> Repo:
        url: str = self.__exec_for_stdout(['git', 'config', '--local', '--get', 'remote.origin.url'])
        regexp: Pattern[str] = re.compile(
            '^git@github\.com:(?P<owner>[\w\d._-]*)/(?P<repo>[\w\d._-]*)\.git$',
            re.IGNORECASE)
        matches: Match = re.match(regexp, url)
        if matches is None:
            raise ValueError(
                'remote.origin.url not match with : ^git@github\.com:(?P<owner>[\w\d._-]*)/(?P<repo>[\w\d._-]*)\.git$')
        return Repo(owner=matches.groupdict().get('owner'), repo=matches.groupdict().get('repo'))

    def get_current_branch_name(self) -> str:
        # git branch --no-color | grep '^\* ' | grep -v 'no branch' | sed 's/^* //g'
        return self.__exec_for_stdout(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])

    def has_conflict(self) -> bool:
        return len(self.get_conflict()) > 0

    def has_head(self) -> bool:
        return len(self.__exec_for_stdout(['git', 'show-ref', '--heads'])) > 0

    def is_local_remote_equal(self, branch: str) -> bool:
        if self.branch_exists(branch):
            raise BranchNotExist(branch)

        local_branch: str = self.local_branch_name(branch)
        remote_branch: str = self.remote_branch_name(branch)
        compare_refs: int = self.compare_refs(local_branch, remote_branch)

        if compare_refs > 0:
            print("Branches '{local_branch!s}' and '{remote_branch!s}' have diverged.".format(local_branch=local_branch,
                                                                                              remote_branch=remote_branch))
            if compare_refs == 1:
                print("And branch '{local_branch!s}' may be fast-forwarded.".format(local_branch=local_branch))
            elif compare_refs == 2:
                print("And local branch '{local_branch!s}' is ahead of '{remote_branch!s}'.".format(
                    local_branch=local_branch,
                    remote_branch=remote_branch
                ))
            else:
                print("Branches need merging first.")
            return False
        return True

    def is_clean_working_tree(self) -> bool:
        if len(self.__exec_for_stdout(['git', 'rev-parse', '--verify', 'HEAD'])) == 0:
            return False
        self.__exec(['git', 'update-index', '-q', '--ignore-submodules', '--refresh'])

        if len(self.__exec_for_stdout(['git', 'diff-files', '--ignore-submodules'])) > 0:
            print("Working tree contains unstaged changes. Aborting.")
            return False

        if len(self.__exec_for_stdout(
                ['git', 'diff-index', '--cached', '--ignore-submodules', 'HEAD'])) > 0:
            print("Index contains uncommited changes. Aborting.")
            return False

        return True

    def compare_refs(self, branch1: str, branch2: str) -> int:

        commit1: str = self.__exec_for_stdout(['git', 'rev-parse ', branch1 + '^{}'])
        commit2: str = self.__exec_for_stdout(['git', 'rev-parse ', branch2 + '^{}'])

        if not commit1 == commit2:
            child: Popen = Popen(
                ['git', 'merge-base ', '"{c!s}"'.format(c=commit1), '"{c!s}"'.format(c=commit2)],
                stdout=PIPE,
                cwd=self.__state_handler.dir_path.as_posix()
            )

            stdout, stderr = child.communicate()
            base: str = self.__decode_stdout(stdout)

            if not child.returncode == 0:
                return 4
            elif commit1 == base:
                return 1
            elif commit2 == base:
                return 2
            else:
                return 3
        else:
            return 0

    def init_head(self) -> GitCmd:
        self.__exec(['git', 'symbolic-ref', 'HEAD', '"refs/heads/' + Branches.MASTER.value + '"'])
        return self

    def has_remote(self) -> bool:
        try:
            repo: Repo = self.get_repo()
            return True
        except ValueError:
            return False

    def last_tag(self) -> str:
        return self.__exec_for_stdout(['git', 'describe', '--abbrev=0', '--tags'])

    def merge(self, branch: Branches, options: List[str] = []) -> GitCmd:
        target_branch_name: str = self.get_branch_name_from_git(branch)
        self.__exec(['git', 'merge', target_branch_name, *options])
        self.__state_handler.load_file_config()
        return self

    def merge_with_version_message(self, branch: Branches, message: str = '', options: List[str] = []) -> GitCmd:
        commit_message: str = """merge : {branch_name!s}
    {message!s}""".format(branch_name=self.get_branch_name_from_git(branch), message=message)
        return self.merge(
            branch,
            options=['--commit', '-m', commit_message, *options]
        )

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
        self.__exec(['git', 'push', '-u', '--force', GitConfig.REMOTE.value, self.get_current_branch_name()])
        return self

    def tag_exists(self, tag: str, remote: bool) -> bool:
        if remote:
            resp: str = self.__exec_for_stdout(['git', 'ls-remote', GitConfig.REMOTE.value, 'refs/tags/' + tag])
            return len(resp) > 0 and re.match(re.compile('.*refs/tags/' + tag + '$'), resp) is not None
        else:
            p1 = Popen(
                ['git', 'tag', '-l'],
                stdout=PIPE,
                cwd=self.__state_handler.dir_path.as_posix()
            )

            p2 = Popen(
                ['grep', '-E', tag],
                stdin=p1.stdout,
                stdout=PIPE,
                cwd=self.__state_handler.dir_path.as_posix())
            p1.stdout.close()
            result = p2.communicate()[0]
            p1.wait()

            resp = self.__decode_stdout(result)

            return len(resp) > 0 and re.match(re.compile('^' + tag + '$'), resp) is not None

    def reset_to_tag(self, tag: str) -> GitCmd:
        self.__exec(['git', 'reset', '--hard', tag])
        return self

    def set_upstream(self) -> GitCmd:
        self.__exec(["git", "push", "--set-upstream", GitConfig.REMOTE.value, self.get_current_branch_name()])
        return self

    def try_to_pull(self) -> GitCmd:
        print('Try to pull')
        if self.has_remote():
            return self.pull()
        return self

    def try_to_push(self) -> GitCmd:
        print('Try to push')
        if self.has_remote():
            return self.push()
        return self

    def try_to_push_force(self) -> GitCmd:
        print('Try to push')
        if self.has_remote():
            return self.push_force()
        return self

    def try_to_push_tag(self, tag: str) -> GitCmd:
        print('Try to push tag')
        if self.has_remote():
            return self.push_tag(tag)
        return self

    def try_to_set_upstream(self) -> GitCmd:
        print('Try to set upstream')
        if self.has_remote():
            return self.set_upstream()
        return self

    def tag(self, tag: str, msg: Optional[str] = None) -> GitCmd:
        msg = msg if msg else tag
        self.__exec(["git", "tag", "-a", tag, "-m", "'" + msg + "'"])
        return self

    def local_branch_name(self, branch: Optional[str] = None) -> str:
        base: str = 'refs/heads'
        if branch is not None:
            return base + '/{branch!s}'.format(branch=branch)
        else:
            return base

    def remote_branch_name(self, branch: Optional[str] = None) -> str:
        base: str = 'refs/remotes'
        if branch is not None:
            return base + '/{branch!s}'.format(branch=branch)
        else:
            return base
