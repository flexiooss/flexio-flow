import unittest
from tests.Schemes.Package.TestPackageScheme import TestPackageScheme

def suite():
    suite = unittest.TestSuite()
    # suite.addTest(TestFlexioFlowConfig('bibi'))
    suite.addTest(TestPackageScheme('bubu'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
