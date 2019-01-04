import unittest
import os

from Schemes.Dependencies import Dependencies
from Schemes.Maven.ReportFileReader import ReportFileReader
from Exceptions.ParseFailureException import ParseFailureException


class TestReportFileReader(unittest.TestCase):

    def test_given_report_file_doesnt_exists__then_dependencies_is_empty(self):
        reader: ReportFileReader = ReportFileReader('/no/such/file')

        deps: Dependencies = reader.read()

        self.assertIs(len(deps), 0)

    def test_given_report_rile_exists__when_report_is_empty__then_dependencies_is_empty(self):
        reader: ReportFileReader = ReportFileReader(self.ressource_path('empty-report.txt'))

        deps: Dependencies = reader.read()

        self.assertIs(len(deps), 0)

    def test_given_report_file_exists__when_report_contains_one_parseable_line__then_dependencies_has_one_element(self):
        reader: ReportFileReader = ReportFileReader(self.ressource_path('one-dep-report.txt'))

        deps: Dependencies = reader.read()

        self.assertIs(len(deps), 1)
        self.assertTupleEqual(deps.to_list()[0], ('com.fasterxml.jackson.core:jackson-core', '2.8.8-SNAPSHOT'))

    def test_given_report_file_exists__when_report_contains_many_parseable_line__then_dependencies_has_many_elements(self):
        reader: ReportFileReader = ReportFileReader(self.ressource_path('many-deps-report.txt'))

        deps: Dependencies = reader.read()

        self.assertIs(len(deps), 4)

    def test_given_report_file_exists__when_report_contains_one_unparseable_line__then_dependencies_has_one_element(self):
        reader: ReportFileReader = ReportFileReader(self.ressource_path('unparseable-dep-report.txt'))

        with self.assertRaises(ParseFailureException):
            reader.read()

    def ressource_path(self, resource):
        return os.path.dirname(os.path.realpath(__file__)) + '/resources/' + resource
