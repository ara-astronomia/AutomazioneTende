from enum import Enum
import config

class GPIOPin(Enum):

    VERIFY_CLOSED = config.Config.getValue("roof_verify_closed", "roof_board")
    VERIFY_OPEN = config.Config.getValue("roof_verify_open", "roof_board")
    SWITCH_ROOF = config.Config.getValue("switch_roof", "roof_board")
