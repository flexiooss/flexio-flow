import unittest
from tests.Schemes.Package.TestPackageScheme import TestPackageScheme
from tests.FlexioFlow.TestVersion import TestVersion


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestVersion())
    suite.addTest(TestPackageScheme())
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
