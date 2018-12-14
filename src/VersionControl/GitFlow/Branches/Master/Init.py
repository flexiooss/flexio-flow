from __future__ import annotations
from FlexioFlow.Level import Level
from FlexioFlow.StateHandler import StateHandler
from Schemes.UpdateSchemeVersion import UpdateSchemeVersion
from VersionControl.Branches import Branches
from VersionControl.GitFlow.Branches.GitFlowCmd import GitFlowCmd
from VersionControl.GitFlow.GitCmd import GitCmd


class Init:
    def __init__(self, state_handler: StateHandler):
        self.__state_handler: StateHandler = state_handler

    def __init_gitflow(self) -> Init:
        GitFlowCmd(self.__state_handler).init_config()
        return self

    def __init_master(self) -> Init:
        version: str = str(self.__state_handler.state.version)

        git: GitCmd = GitCmd(self.__state_handler)
        git.checkout(Branches.MASTER)

        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)

        git.add_all().commit(
            ''.join(["'Init master : ", version, "'"])).tag(version).set_upstream()

        print('Init master at : ' + version)
        git.push_tag(version)
        print('Tag master at : ' + version)
        return self

    def __init_develop(self) -> Init:
        self.__state_handler.state.next_dev_minor()
        version: str = '-'.join([str(self.__state_handler.state.version), Level.DEV.value])

        git: GitCmd = GitCmd(self.__state_handler)
        git.checkout(Branches.DEVELOP)

        self.__state_handler.write_file()
        UpdateSchemeVersion.from_state_handler(self.__state_handler)

        git.add_all().commit(
            ''.join(["'Init develop : ", version, "'"])
        ).tag(version).set_upstream()

        print('Init develop at : ' + version)
        git.push_tag(version)
        print('Tag master at : ' + version)

        return self

    def process(self):
        # root_path, stderr = Popen(["pwd"], stdout=PIPE).communicate()
        #
        # os.chdir(self.__state_handler.dir_path.as_posix())

        self.__init_gitflow().__init_master().__init_develop()

        # os.chdir(root_path.strip())
