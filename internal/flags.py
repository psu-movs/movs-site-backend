from enum import IntFlag


class Permissions(IntFlag):
    NONE = 0
    MANAGE_NEWS = 1 << 0
    MANAGE_TEACHERS = 1 << 1
    MANAGE_INFO = 1 << 2
    ADMINISTRATOR = 1 << 3
