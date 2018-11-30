import unittest
from tests.TestFlexioFlowConfig import TestFlexioFlowConfig


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestFlexioFlowConfig('bibi'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
