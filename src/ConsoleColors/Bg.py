from enum import Enum, unique


@unique
class Bg(Enum):
    RESET: str = '\x1b[0m'
    INFO: str = '\033[46m' + '\033[90m'
    NOTICE: str = '\033[103m' + '\033[90m'
    FOCUS: str = '\033[105m' + '\033[90m'
    WARNING: str = '\033[43m' + '\033[90m'
    FAIL: str = '\033[41m' + '\033[90m'
    SUCCESS: str = '\033[42m' + '\033[90m'
