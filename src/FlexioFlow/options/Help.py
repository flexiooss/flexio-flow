import os
import sys
from FlexioFlow.options.Option import Option


class Help(Option):
    HAS_VALUE = False
    SHORT_NAME = 'H'
    NAME = 'help'

    def exec(self):
        file = open(os.path.dirname(os.path.abspath(__file__)) + '/../../help.txt', 'r')
        print(file.read())
        sys.exit()
