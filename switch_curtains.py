import config
from time import sleep
from status import Status
from transition_error import TransitionError
from gpio_pin import GPIOPin
from base.singleton import Singleton
from gpio_config import GPIOConfig

class SwitchCurtains:
    def __init__(self):
        self.gpioconfig = GPIOConfig()

class EstSwitchCurtain(SwitchCurtains, metaclass=Singleton):
    def read(self):
        is_curtain_E_closed = self.gpioconfig.status(GPIOPin.CURTAINS_VERIFY_CLOSED_E)
        is_curtain_E_open = self.gpioconfig.status(GPIOPin.CURTAINS_VERIFY_OPEN_E)

        if is_curtain_E_closed and is_curtain_E_open:
            raise TransitionError("""curtain_E state invalid - La Tenda Est è
            in uno stato invalido""")
        elif is_curtain_E_closed:
            return Status.CURTAIN_E_CLOSED
        elif is_curtain_E_open:
            return Status.CURTAIN_E_OPEN

class WestSwitchCurtain(SwitchCurtains, metaclass=Singleton):
    def read(self):
        is_curtain_W_closed = self.gpioconfig.status(GPIOPin.CURTAINS_VERIFY_CLOSED_W)
        is_curtain_W_open = self.gpioconfig.status(GPIOPin.CURTAINS_VERIFY_OPEN_W)

        if is_curtain_W_closed and is_curtain_W_open:
            raise TransitionError("""Roof state invalid - La chiusura del tetto è
            in uno stato invalido""")
        elif is_curtain_W_closed:
            return Status.CURTAIN_W_CLOSED
        elif is_curtain_W_open:
            return Status.CURTAIN_W_OPEN
