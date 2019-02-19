from enum import Enum, unique


@unique
class Style(Enum):
    RESET: str = '\x1b[0m'
    BOLD: str = '\033[1m'
    UNDERLINE: str = '\033[4m'
    STRIKETHROUGH: str = '\033[09m'
    REVERSE: str = '\033[07m'
    DISABLE: str = '\033[02m'
