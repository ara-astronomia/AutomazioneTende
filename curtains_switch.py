import config
from time import sleep
from status import Status
from transition_error import TransitionError
from gpio_pin import GPIOPin
from base.singleton import Singleton
from gpio_config import GPIOConfig

class CurtainSwitch:
    def __init__(self):
        self.gpioconfig = GPIOConfig()

class CurtainEstSwitch(CurtainSwitch, metaclass=Singleton):
    def read(self):
        is_curtain_E_closed = self.gpioconfig.status(GPIOPin.CURTAIN_E_VERIFY_CLOSED)
        is_curtain_E_open = self.gpioconfig.status(GPIOPin.CURTAIN_E_VERIFY_OPEN)

        if is_curtain_E_closed and is_curtain_E_open:
            raise TransitionError("""curtain_E state invalid - La Tenda Est è
            in uno stato invalido""")
        elif is_curtain_E_closed:
            return Status.CURTAIN_E_CLOSED
        elif is_curtain_E_open:
            return Status.CURTAIN_E_OPEN

class CurtainWestSwitch(CurtainSwitch, metaclass=Singleton):
    def read(self):
        is_curtain_W_closed = self.gpioconfig.status(GPIOPin.CURTAIN_W_VERIFY_CLOSED)
        is_curtain_W_open = self.gpioconfig.status(GPIOPin.CURTAIN_W_VERIFY_OPEN)

        if is_curtain_W_closed and is_curtain_W_open:
            raise TransitionError("""Roof state invalid - La chiusura del tetto è
            in uno stato invalido""")
        elif is_curtain_W_closed:
            return Status.CURTAIN_W_CLOSED
        elif is_curtain_W_open:
            return Status.CURTAIN_W_OPEN
