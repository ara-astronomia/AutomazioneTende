from enum import Enum
from config import Config

class GPIOPin(Enum):

    VERIFY_CLOSED = Config.getValue("roof_verify_closed", "roof_board")
    VERIFY_OPEN = Config.getValue("roof_verify_open", "roof_board")
    SWITCH_ROOF = Config.getValue("switch_roof", "roof_board")
