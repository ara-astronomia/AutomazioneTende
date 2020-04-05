from enum import Enum
from config import Config
import RPi.GPIO as GPIO # type: ignore

class GPIOPin(Enum):
    #impostazione gpio switch e comando tetto
    VERIFY_CLOSED = (Config.getInt("roof_verify_closed", "roof_board"), GPIO.IN, GPIO.PUD_UP)
    VERIFY_OPEN = (Config.getInt("roof_verify_open", "roof_board"), GPIO.IN, GPIO.PUD_UP)
    SWITCH_ROOF = (Config.getInt("switch_roof", "roof_board"), GPIO.OUT)

    #impostazione gpio switch fine_corsa tende
    CURTAIN_W_VERIFY_OPEN = (Config.getInt("curtain_W_verify_open", "curtains_limit_switch"), GPIO.IN, GPIO.PUD_UP)
    CURTAIN_W_VERIFY_CLOSED= (Config.getInt("curtain_W_verify_closed", "curtains_limit_switch"), GPIO.IN, GPIO.PUD_UP)
    CURTAIN_E_VERIFY_OPEN = (Config.getInt("curtain_E_verify_open", "curtains_limit_switch"), GPIO.IN, GPIO.PUD_UP)
    CURTAIN_E_VERIFY_CLOSED = (Config.getInt("curtain_E_verify_closed", "curtains_limit_switch"), GPIO.IN, GPIO.PUD_UP)

    MOTORE_A = (Config.getInt("motorE_A", "motor_board"), GPIO.OUT)
    MOTORE_B = (Config.getInt("motorE_B", "motor_board"), GPIO.OUT)
    MOTORE_E = (Config.getInt("motorE_E", "motor_board"), GPIO.OUT)
    MOTORW_A = (Config.getInt("motorW_A", "motor_board"), GPIO.OUT)
    MOTORW_B = (Config.getInt("motorW_B", "motor_board"), GPIO.OUT)
    MOTORW_E = (Config.getInt("motorW_E", "motor_board"), GPIO.OUT)

    CLK_E = (Config.getInt("clk_e", "encoder_board"), GPIO.IN, GPIO.PUD_UP)
    DT_E = (Config.getInt("dt_e", "encoder_board"), GPIO.IN, GPIO.PUD_UP)
    CLK_W = (Config.getInt("clk_w", "encoder_board"), GPIO.IN, GPIO.PUD_UP)
    DT_W = (Config.getInt("dt_w", "encoder_board"), GPIO.IN, GPIO.PUD_UP)

    def __init__(self, id_pin, pin_setup, pull=None):
        self.id_pin = id_pin
        self.pin_setup = pin_setup
        self.pull = pull

    @staticmethod
    def setup(mode=GPIO.BOARD):
        GPIO.setmode(mode)
        for pin in list(GPIOPin):
            if pin.pull:
                GPIO.setup(pin.id_pin, pin.pin_setup, pull_up_down=pin.pull)
            else:
                GPIO.setup(pin.id_pin, pin.pin_setup)
