import unittest
import os
from pathlib import Path
import shutil
from FlexioFlow.State import State
from FlexioFlow.Version import Version
from FlexioFlow.Level import Level
from Schemes.Schemes import Schemes
from Schemes.Package.PackageFileHandler import PackageFileHandler
from pathlib import Path
from tests.Schemes.Package.TestPackageHelper import TestPackageHelper
from pathlib import Path
from FlexioFlow.StateHandler import StateHandler
from subprocess import PIPE, Popen
from VersionControl.GitFlow.GitFlow import GitFlow
from VersionControl.Branches import Branches
from tests.VersionControl.GitFlow.TestGitFlowHelper import TestGitFlowHelper


class TestGitFlow(unittest.TestCase):
    def test_should_remote_tag_exists(self):
        raise Exception('not implemented')

