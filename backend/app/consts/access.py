from enum import IntEnum


class AccessLevel(IntEnum):
    FORBIDDEN = 0
    READ = 1
    READ_BRANCH = 2
    FULL = 3
    FULL_BRANCH = 4
