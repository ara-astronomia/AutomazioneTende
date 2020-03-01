from enum import IntEnum

class Status(IntEnum):

    # static statuses have lower values
    CLOSED = 1
    STOPPED = 2
    OPEN = 3

    # movement statuses have higher values
    CLOSING = 4
    OPENING = 5

    # danger zone - threat it as a movement statuses (but we hope it has stopped)
    # user should manually reset the steps after checking visually the curtains status
    DANGER = 6
