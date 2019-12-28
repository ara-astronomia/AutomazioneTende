from enum import IntEnum

class Status(IntEnum):

    OPEN = 1
    CLOSED = 2
    OPENING = 3
    CLOSING = 4

class CurtainStatus(IntEnum):

    OPENING = 1
    CLOSING = 2
    STOPPED = 3
