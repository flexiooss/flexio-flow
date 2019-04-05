from __future__ import annotations

import logging
import sys

FlexLogger = logging.getLogger('FlexioFlow')
FlexLogger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] : %(message)s')
handler.setFormatter(formatter)
FlexLogger.addHandler(handler)


class Log:

    @staticmethod
    def info(mes: str):
        FlexLogger.info(mes)

    @staticmethod
    def warning(mes: str):
        FlexLogger.warning(mes)

    @staticmethod
    def critical(mes: str):
        FlexLogger.critical(mes)

    @staticmethod
    def error(mes: str):
        FlexLogger.error(mes)

    @staticmethod
    def exception(mes: str):
        FlexLogger.exception(mes)
