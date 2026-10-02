import unittest
from pathlib import Path

from Branches.Actions.Start import Start
from Branches.Branches import Branches
from Branches.BranchesConfig import BranchesConfig
from Core.Config import Config
from Core.ConfigHandler import ConfigHandler
from Exceptions.FromTagRequired import FromTagRequired
from FlexioFlow.Options import Options
from FlexioFlow.StateHandler import StateHandler
from VersionControl.Git.Git import Git
from tests.VersionControl.GitFlow.LocalRepo import LocalRepo


class TestSupportStartPrecondition(unittest.TestCase):
    PATH: Path = Path('/tmp/test_flexioflow_precondition')

    def setUp(self):
        LocalRepo.create(self.PATH)
        self.state_handler: StateHandler = StateHandler(self.PATH)
        self.state_handler.load_file_config()
        self.config_handler: ConfigHandler = ConfigHandler(Path('/tmp/test_flexioflow_precondition_config'))
        self.config_handler.config = Config().with_branches_config(BranchesConfig.from_dict({}))

    def tearDown(self):
        LocalRepo.clean(self.PATH)

    def __action(self, from_tag=None) -> Start:
        options: Options = Options()
        options.from_tag = from_tag
        options.default = True
        options.no_cli = True
        return Start(
            Git(self.state_handler, self.config_handler),
            Branches.SUPPORT_BRANCH,
            self.state_handler,
            options,
            self.config_handler
        )

    def test_should_refuse_before_building_any_issue_or_topic(self):
        with self.assertRaises(FromTagRequired):
            self.__action().process()
