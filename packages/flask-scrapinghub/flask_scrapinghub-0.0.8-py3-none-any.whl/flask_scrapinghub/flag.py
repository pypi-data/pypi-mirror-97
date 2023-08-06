from enum import Enum


class Color(Enum):
    Red = 1
    GREEN = 2
    YELLOW = 3
    BLACK = 4


class Execution(Enum):
    NO_SPIDER = 1
    FAIL = 2
    SUCCESS = 3
