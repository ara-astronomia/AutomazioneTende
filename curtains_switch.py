import config
from time import sleep
from status import Status
from transition_error import TransitionError
from gpio_pin import GPIOPin
from base.singleton import Singleton
from gpio_config import GPIOConfig
from curtains_control import EastCurtain, WestCurtain

class CurtainSwitch:
    def __init__(self):
        self.gpioconfig = GPIOConfig()

    def read(self):
        is_curtain_open = self.gpioconfig.status(self.curtain_open)
        is_curtain_closed = self.gpioconfig.status(self.curtain_closed)
        if is_curtain_closed and is_curtain_open:
            raise TransitionError("""curtain_E state invalid - La Tenda Est è
            in uno stato invalido""")
        elif is_curtain_open:
            return Status.OPEN
        elif is_curtain_closed:
            return Status.CLOSED
        else:
            return Status.STOPPED

    def close(self):
        self.motor.close()
        self.gpioconfig.wait_for_raising(self.curtain_closed)
        self.motor.stop()

    def open(self):mi
        self.motor.open()
        self.gpioconfig.wait_for_raising(self.curtain_open)
        self.motor.stop()

class CurtainEastSwitch(CurtainSwitch, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.curtain_closed = GPIOPin.CURTAIN_E_VERIFY_CLOSED
        self.curtain_open = GPIOPin.CURTAIN_E_VERIFY_OPEN
        self.motor = EastCurtain()

class CurtainWestSwitch(CurtainSwitch, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.curtain_closed = GPIOPin.CURTAIN_W_VERIFY_CLOSED
        self.curtain_open = GPIOPin.CURTAIN_W_VERIFY_OPEN
        self.motor = WestCurtain()
