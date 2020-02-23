from enum import IntEnum

class RoofStatus(IntEnum):

    OPEN = 1
    CLOSED = 2
    OPENING = 3
    CLOSING = 4

class CurtainStatus(IntEnum):

    OPENING = 1
    CLOSING = 2
    STOPPED = 3

class Status(IntEnum):

    ROOF_CLOSED = 0
    TELESCOPE_PARKED = 1
    # from next state, telescope can operate
    CURTAINS_CLOSED = 2
    CURTAINS_OPEN = 3
