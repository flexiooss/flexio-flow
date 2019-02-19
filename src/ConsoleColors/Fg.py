from enum import Enum, unique


@unique
class Fg(Enum):
    RESET: str = '\x1b[0m'
    INFO: str = '\033[36m'
    NOTICE: str = '\033[93m'
    FOCUS: str = '\033[95m'
    WARNING: str = '\033[33m'
    FAIL: str = '\033[31m'
    SUCCESS: str = '\033[32m'
