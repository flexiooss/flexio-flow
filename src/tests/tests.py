import unittest
from tests.Schemes.Package.TestPackageScheme import TestPackageScheme
from tests.FlexioFlow.TestVersion import TestVersion
from tests.FlexioFlow.TestState import TestState


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestVersion())
    suite.addTest(TestState())
    suite.addTest(TestPackageScheme())
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
