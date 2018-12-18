from __future__ import annotations

from Exceptions.BranchNotExist import BranchNotExist
from FlexioFlow.StateHandler import StateHandler
from Schemes.UpdateSchemeVersion import UpdateSchemeVersion
from VersionControl.Branches import Branches
from VersionControl.GitFlow.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.GitFlow.GitCmd import GitCmd


class Finish:
    def __init__(self, state_handler: StateHandler):
        self.__state_handler: StateHandler = state_handler
        self.__git: GitCmd = GitCmd(self.__state_handler)
        self.__gitflow: GitFlowCmd = GitFlowCmd(self.__state_handler)

    def __init_gitflow(self) -> Finish:
        self.__gitflow.init_config()
        return self

    def __pull_develop(self) -> Finish:
        self.__git.checkout(Branches.DEVELOP).pull()
        return self

    def __pull_master(self) -> Finish:
        self.__git.checkout(Branches.MASTER).pull()
        return self

    def __merge_master(self) -> Finish:
        self.__git.checkout(Branches.MASTER).merge_with_version_message(
            Branches.RELEASE,
            ['--no-ff', '--strategy-option', 'theirs']
        ).tag(
            self.__state_handler.version_as_str(),
            ' '.join([
                "'From Finished release : ",
                self.__git.get_branch_name_from_git(Branches.RELEASE),
                'tag : ',
                self.__state_handler.version_as_str(),
                "'"])
        ).push_tag(self.__state_handler.version_as_str()).push()
        if (self.__git.has_conflict()):
            print('##################################################')
            print('master have conflicts : ')
            print(self.__git.get_conflict())
            print('##################################################')
        return self

    def __merge_develop(self) -> Finish:
        self.__git.checkout_with_branch_name(self.__git.get_branch_name_from_git(Branches.RELEASE))
        self.__state_handler.next_dev_minor()
        self.__state_handler.set_dev()
        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)
        self.__git.commit(''.join(["'Finish release for dev: ", self.__state_handler.version_as_str()])).push()

        self.__git.checkout(Branches.DEVELOP).merge_with_version_message(Branches.RELEASE).push()
        if (self.__git.has_conflict()):
            print('##################################################')
            print('develop have conflicts : ')
            print(self.__git.get_conflict())
            print('##################################################')
        return self

    def __delete_release(self) -> Finish:
        self.__git.delete_branch(Branches.RELEASE, True)
        self.__git.delete_branch(Branches.RELEASE, False)
        return self

    def __finish_release(self):
        if not self.__gitflow.has_release(False):
            raise BranchNotExist(Branches.RELEASE)
        self.__merge_master().__merge_develop().__delete_release()

    def process(self):
        self.__pull_develop().__pull_master().__finish_release()
