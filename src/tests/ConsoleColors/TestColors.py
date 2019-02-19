import unittest

from ConsoleColors.Bg import Bg
from ConsoleColors.Fg import Fg
from ConsoleColors.PrintColor import PrintColor
from ConsoleColors.Style import Style


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
