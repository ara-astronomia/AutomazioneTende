from enum import Enum
from config import Config
from typing import NamedTuple
from enum import IntEnum


class GPIO(IntEnum):
    OUT = 0
    IN = 1
    LOW = 0
    HIGH = 1
    PUD_OFF = 20
    PUD_UP = 22
    BOARD = 10


class Pin(NamedTuple):
    id_pin: int
    pin_setup: int = GPIO.IN
    pull: int = GPIO.PUD_OFF
    on_is: int = GPIO.LOW


class GPIOPin(Pin, Enum):
    # impostazione gpio switch e comando tetto
    VERIFY_CLOSED = Pin(Config.getInt("roof_verify_closed", "roof_board"), GPIO.IN, pull=GPIO.PUD_UP)
    VERIFY_OPEN = Pin(Config.getInt("roof_verify_open", "roof_board"), GPIO.IN, pull=GPIO.PUD_UP)
    SWITCH_ROOF = Pin(Config.getInt("switch_roof", "roof_board"), GPIO.OUT, on_is=Config.getInt("switch_roof_open", "roof_board"))

    # impostazione gpio panel flat
    SWITCH_PANEL = Pin(Config.getInt("switch_panel", "panel_board"), GPIO.OUT, on_is=Config.getInt("switch_on", "panel_board"))
    # impostazione gpio alimentatore
    SWITCH_POWER_TELE = Pin(Config.getInt("switch_power", "panel_board"), GPIO.OUT, on_is=Config.getInt("switch_power_on_tele", "panel_board"))
    # impostazione gpio luci cupola
    SWITCH_LIGHT = Pin(Config.getInt("switch_light", "panel_board"), GPIO.OUT, on_is=Config.getInt("switch_light_on", "panel_board"))
    # impostazione gpio auxiliary
    SWITCH_POWER_CCD = Pin(Config.getInt("switch_aux", "panel_board"), GPIO.OUT, on_is=Config.getInt("switch_power_on_ccd", "panel_board"))

    # impostazione gpio switch fine_corsa tende
    CURTAIN_W_VERIFY_OPEN = Pin(Config.getInt("curtain_W_verify_open", "curtains_limit_switch"), GPIO.IN, pull=GPIO.PUD_UP)
    CURTAIN_W_VERIFY_CLOSED = Pin(Config.getInt("curtain_W_verify_closed", "curtains_limit_switch"), GPIO.IN, pull=GPIO.PUD_UP)
    CURTAIN_E_VERIFY_OPEN = Pin(Config.getInt("curtain_E_verify_open", "curtains_limit_switch"), GPIO.IN, pull=GPIO.PUD_UP)
    CURTAIN_E_VERIFY_CLOSED = Pin(Config.getInt("curtain_E_verify_closed", "curtains_limit_switch"), GPIO.IN, pull=GPIO.PUD_UP)

    MOTORE_A = Pin(Config.getInt("motorE_A", "motor_board"), GPIO.OUT, on_is=Config.getInt("switch_roof_open", "roof_board"))
    MOTORE_B = Pin(Config.getInt("motorE_B", "motor_board"), GPIO.OUT, on_is=Config.getInt("switch_roof_open", "roof_board"))
    MOTORE_E = Pin(Config.getInt("motorE_E", "motor_board"), GPIO.OUT, on_is=Config.getInt("switch_roof_open", "roof_board"))
    MOTORW_A = Pin(Config.getInt("motorW_A", "motor_board"), GPIO.OUT, on_is=Config.getInt("switch_roof_open", "roof_board"))
    MOTORW_B = Pin(Config.getInt("motorW_B", "motor_board"), GPIO.OUT, on_is=Config.getInt("switch_roof_open", "roof_board"))
    MOTORW_E = Pin(Config.getInt("motorW_E", "motor_board"), GPIO.OUT, on_is=Config.getInt("switch_roof_open", "roof_board"))

    @staticmethod
    def setup():
        import RPi.GPIO  # type: ignore
        RPi.GPIO.setmode(RPi.GPIO.BOARD)
        for pin in list(GPIOPin):
            if pin.pull:
                RPi.GPIO.setup(pin.id_pin, pin.pin_setup, pull_up_down=pin.pull)
            else:
                RPi.GPIO.setup(pin.id_pin, pin.pin_setup)
