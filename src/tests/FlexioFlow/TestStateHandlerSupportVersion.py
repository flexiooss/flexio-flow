import shutil
import unittest
from pathlib import Path

from FlexioFlow.StateHandler import StateHandler


class TestStateHandlerSupportVersion(unittest.TestCase):
    PATH: Path = Path('/tmp/test_flexioflow_state')

    def setUp(self):
        shutil.rmtree(self.PATH.as_posix(), True)
        self.PATH.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.PATH.as_posix(), True)

    def __write(self, version: str) -> StateHandler:
        (self.PATH / 'flexio-flow.yml').write_text(
            'level: dev\nschemes: []\ntopics: []\nversion: ' + version + '\n')
        return StateHandler(self.PATH).load_file_config()

    def test_should_read_and_rewrite_a_three_component_file_unchanged(self):
        handler: StateHandler = self.__write('1.29.0')
        handler.write_file()
        content: str = (self.PATH / 'flexio-flow.yml').read_text()
        self.assertIn('version: 1.29.0', content)
        self.assertNotIn('support', content)

    def test_should_read_and_rewrite_a_four_component_file(self):
        handler: StateHandler = self.__write('1.29.0.1')
        handler.write_file()
        self.assertIn('version: 1.29.0.1', (self.PATH / 'flexio-flow.yml').read_text())

    def test_should_bump_support_through_the_handler(self):
        handler: StateHandler = self.__write('1.29.0')
        handler.next_dev_support()
        self.assertEqual('1.29.0.1', handler.version_as_str())
