from enum import Enum
from config import Config
import RPi.GPIO as GPIO

class GPIOPin(Enum):
    #impostazione gpio switch e comando tetto
    VERIFY_CLOSED = (Config.getValue("roof_verify_closed", "roof_board"), GPIO.OUT)
    VERIFY_OPEN = (Config.getValue("roof_verify_open", "roof_board"), GPIO.IN, GPIO.PUD_UP)
    SWITCH_ROOF = (Config.getValue("switch_roof", "roof_board"), GPIO.IN, GPIO.PUD_UP)

    #impostazione gpio switch fine_corsa tende
    CURTAINS_VERIFY_OPEN_W = (Config.getValue("curtains_verify_open_W", "fine_corsa_curtains"), GPIO.IN, GPIO.PUD_UP)
    CURTAINS_VERIFY_CLOSED_W = (Config.getValue("curtains_verify_closed_W", "fine_corsa_curtains"), GPIO.OUT)
    CURTAINS_VERIFY_OPEN_E = (Config.getValue("curtains_verify_open_E", "fine_corsa_curtains"), GPIO.IN, GPIO.PUD_UP)
    CURTAINS_VERIFY_CLOSED_E = (Config.getValue("curtains_verify_closed_E", "fine_corsa_curtains"), GPIO.OUT)

    MOTORE_A = (Config.getValue("motorE_A", "motor_board"), GPIO.OUT)
    MOTORE_B = (Config.getValue("motorE_B", "motor_board"), GPIO.OUT)
    MOTORE_E = (Config.getValue("motorE_E", "motor_board"), GPIO.OUT)
    MOTORW_A = (Config.getValue("motorW_A", "motor_board"), GPIO.OUT)
    MOTORW_B = (Config.getValue("motorW_B", "motor_board"), GPIO.OUT)
    MOTORW_E = (Config.getValue("motorW_E", "motor_board"), GPIO.OUT)

    CLK_E = (Config.getValue("clk_e", "encoder_board"), GPIO.IN, GPIO.PUD_UP)
    DT_E = (Config.getValue("dt_e", "encoder_board"), GPIO.IN, GPIO.PUD_UP)
    CLK_W = (Config.getValue("clk_w", "encoder_board"), GPIO.IN, GPIO.PUD_UP)
    DT_W = (Config.getValue("dt_w", "encoder_board"), GPIO.IN, GPIO.PUD_UP)

    def __init__(self, id_pin, setup, pull=None):
        self.id_pin = id_pin
        self.setup = setup
        self.pull = pull

    @staticmethod
    def setup(mode=GPIO.BOARD):
        GPIO.setmode(mode)
        for pin in list(GPIOPin):
            if pin.pull:
                GPIO.setup(pin.id_pin, pin.setup, pull_up_down=pin.pull)
            else:
                GPIO.setup(pin.id_pin, pin.setup)
