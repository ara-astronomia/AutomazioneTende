from enum import IntEnum

class Status(IntEnum):

    OPEN = 1
    CLOSED = 2
    TRANSIT = 3

class CurtainStatus(IntEnum):

    OPENING = 1
    CLOSING = 2
    STOPPED = 3
