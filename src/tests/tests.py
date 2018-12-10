import unittest
from tests.Schemes.Package.TestPackageScheme import TestPackageScheme
from tests.FlexioFlow.TestVersion import TestVersion
from tests.FlexioFlow.TestState import TestState
from tests.FlexioFlow.Actions.TestPreCheck import TestPreCheck


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestVersion())
    suite.addTest(TestState())
    suite.addTest(TestPreCheck())
    suite.addTest(TestPackageScheme())
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
