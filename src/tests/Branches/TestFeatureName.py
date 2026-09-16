import unittest
from typing import List

from Branches.Actions.FeatureName import FeatureName
from Exceptions.NoFeatureName import NoFeatureName
from FlexioFlow.Options import Options
from FlexioFlow.options.Resolver import Resolver


class TestFeatureName(unittest.TestCase):

    def __options(self, **kwargs) -> Options:
        options: Options = Options()
        options.branch_name = kwargs.get('branch_name', None)
        options.default = kwargs.get('default', False)
        options.no_cli = kwargs.get('no_cli', False)
        return options

    def __never_read(self, message: str) -> str:
        raise AssertionError('should not prompt : ' + message)

    def test_option_wins_over_default(self):
        name: str = FeatureName(
            self.__options(branch_name='fix-4283'),
            'titre-de-l-issue',
            self.__never_read
        ).resolve()
        self.assertEqual(name, 'fix-4283')

    def test_option_does_not_prompt_even_interactive(self):
        name: str = FeatureName(
            self.__options(branch_name='fix-4283'),
            '',
            self.__never_read
        ).resolve()
        self.assertEqual(name, 'fix-4283')

    def test_interactive_uses_typed_name(self):
        name: str = FeatureName(
            self.__options(),
            'titre-de-l-issue',
            lambda message: 'saisi-a-la-main'
        ).resolve()
        self.assertEqual(name, 'saisi-a-la-main')

    def test_interactive_empty_falls_back_on_default(self):
        name: str = FeatureName(
            self.__options(),
            'titre-de-l-issue',
            lambda message: ''
        ).resolve()
        self.assertEqual(name, 'titre-de-l-issue')

    def test_interactive_empty_without_default_raises(self):
        with self.assertRaises(NoFeatureName):
            FeatureName(
                self.__options(),
                '',
                lambda message: ''
            ).resolve()

    def test_default_option_uses_issue_name_without_prompting(self):
        name: str = FeatureName(
            self.__options(default=True),
            'titre-de-l-issue',
            self.__never_read
        ).resolve()
        self.assertEqual(name, 'titre-de-l-issue')

    def test_default_option_without_issue_raises(self):
        with self.assertRaises(NoFeatureName):
            FeatureName(
                self.__options(default=True),
                '',
                self.__never_read
            ).resolve()

    def test_no_cli_option_without_issue_raises(self):
        with self.assertRaises(NoFeatureName):
            FeatureName(
                self.__options(no_cli=True),
                '',
                self.__never_read
            ).resolve()

    def test_no_feature_name_is_a_value_error(self):
        self.assertTrue(issubclass(NoFeatureName, ValueError))

    def test_resolver_parses_branch_name(self):
        options: Options = self.__options()
        Resolver().resolve(opt='--branch-name', arg='fix-4283', options=options)
        self.assertEqual(options.branch_name, 'fix-4283')

    def test_resolver_declares_branch_name_as_valued_option(self):
        names: List[str] = Resolver().name_options()
        self.assertIn('branch-name=', names)
