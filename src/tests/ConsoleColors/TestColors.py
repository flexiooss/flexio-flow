import sys
import unittest

from ConsoleColors.Bg import Bg
from ConsoleColors.Fg import Fg
from ConsoleColors.PrintColor import PrintColor
from ConsoleColors.Style import Style
import logging


class TestColors(unittest.TestCase):

    def test_fg(self):
        for item in Fg:
            print(item)
            PrintColor.log(item.value + 'FlexioFlow')

    def test_bg(self):
        for item in Bg:
            print(item)
            PrintColor.log(item.value + 'FlexioFlow')

    def test_style(self):
        for item in Style:
            print(item)
            PrintColor.log(item.value + 'FlexioFlow')

    def test_logging(self):
        log = logging.getLogger('FlexioFlow')
        log.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] : %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.info(msg='my log')

