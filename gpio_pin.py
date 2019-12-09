from enum import Enum
from config import Config
import RPi.GPIO as GPIO

class GPIOPin(Enum):

    VERIFY_CLOSED = (Config.getValue("roof_verify_closed", "roof_board"), GPIO.OUT)
    VERIFY_OPEN = (Config.getValue("roof_verify_open", "roof_board"), GPIO.IN, GPIO.PUD_UP)
    SWITCH_ROOF = (Config.getValue("switch_roof", "roof_board"), GPIO.IN, GPIO.PUD_UP)

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
