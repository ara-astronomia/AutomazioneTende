from status import Status
from transition_error import TransitionError
from base.singleton import Singleton
from gpio_pin import GPIOPin
from logger import Logger
from gpio_config import GPIOConfig

class CurtainControl:

    def __init__(self):
        self.gpioconfig = GPIOConfig()

    def open(self):
        self.gpioconfig.turn_on(self.pinA)
        self.gpioconfig.turn_off(self.pinB)
        self.gpioconfig.turn_on(self.pinE)
        return self.read()

    def close(self):
        self.gpioconfig.turn_off(self.pinA)
        self.gpioconfig.turn_on(self.pinB)
        self.gpioconfig.turn_on(self.pinE)
        return self.read()

    def stop(self):
        self.gpioconfig.turn_off(self.pinA)
        self.gpioconfig.turn_off(self.pinB)
        self.gpioconfig.turn_off(self.pinE)
        return self.read()

    def read(self):
        self.is_open = self.gpioconfig.status(self.pinA)
        self.is_close = self.gpioconfig.status(self.pinB)
        self.is_enable = self.gpioconfig.status(self.pinE)
        if self.is_open and self.is_enable and not self.is_close:
            return Status.OPENING
        elif self.is_enable and self.is_close and not self.is_open:
            return Status.CLOSING
        elif not self.is_enable:
            return Status.STOPPED
        else:
            raise TransitionError("""Curtain state invalid - La tenda è
            in uno stato invalido""")

class EastCurtain(CurtainControl, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.pinA = GPIOPin.MOTORE_A
        self.pinB = GPIOPin.MOTORE_B
        self.pinE = GPIOPin.MOTORE_E

class WestCurtain(CurtainControl, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.pinA = GPIOPin.MOTORW_A
        self.pinB = GPIOPin.MOTORW_B
        self.pinE = GPIOPin.MOTORW_E
