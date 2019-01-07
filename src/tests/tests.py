import unittest
# from tests.Schemes.Package.TestPackageScheme import TestPackageScheme
# from tests.FlexioFlow.TestVersion import TestVersion
# from tests.FlexioFlow.TestState import TestState
# from tests.FlexioFlow.Actions.TestPreCheck import TestPreCheck
# from tests.VersionControl.Git.TestGitFlow import TestGitFlow
# from tests.VersionControl.Git.TestGitFlowHotfix import TestGitFlowHotfix
# from tests.VersionControl.Git.TestGitFlowInit import TestGitFlowInit
from tests.Schemes.Maven.TestReportFileReader import TestReportFileReader


def suite():
    suite = unittest.TestSuite()
    # suite.addTest(TestVersion())
    # suite.addTest(TestState())
    # suite.addTest(TestPreCheck())
    # suite.addTest(TestPackageScheme())
    # suite.addTest(TestGitFlow())
    # suite.addTest(TestGitFlowInit())
    # suite.addTest(TestGitFlowHotfix())
    suite.addTest(TestReportFileReader())
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
