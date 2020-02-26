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
        if self.is_curtain_closed and self.is_curtain_open:
            raise TransitionError("""curtain_E state invalid - La Tenda Est è
            in uno stato invalido""")
        elif self.is_curtain_open:
            return Status.OPEN
        elif self.is_curtain_closed:
            return Status.CLOSED
        else:
            return Status.STOPPED

    def close(self):
        #pass
        self.motor.close()
        return self.is_verify_close

    def open(self):
        #pass
        self.motor.open()
        return self.is_verify_open


    def __stop__(self):
        pass

class CurtainEastSwitch(CurtainSwitch, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.is_curtain_closed = self.gpioconfig.status(GPIOPin.CURTAIN_E_VERIFY_CLOSED)
        self.is_curtain_open = self.gpioconfig.status(GPIOPin.CURTAIN_E_VERIFY_OPEN)
        self.is_verify_open = self.gpioconfig.wait_for_falling(GPIOPin.CURTAIN_E_VERIFY_OPEN)
        self.is_verify_close = self.gpioconfig.wait_for_falling(GPIOPin.CURTAIN_E_VERIFY_CLOSED)
        self.motor = EastCurtain()

class CurtainWestSwitch(CurtainSwitch, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.is_curtain_closed = self.gpioconfig.status(GPIOPin.CURTAIN_W_VERIFY_CLOSED)
        self.is_curtain_open = self.gpioconfig.status(GPIOPin.CURTAIN_W_VERIFY_OPEN)
        self.is_verify_open = self.gpioconfig.wait_for_falling(GPIOPin.CURTAIN_W_VERIFY_OPEN)
        self.is_verify_close = self.gpioconfig.wait_for_falling(GPIOPin.CURTAIN_W_VERIFY_CLOSED)
        self.motor = WestCurtain()
