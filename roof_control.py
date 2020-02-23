import config
from time import sleep
from status import RoofStatus
from transition_error import TransitionError
from gpio_pin import GPIOPin
from base.singleton import Singleton
from gpio_config import GPIOConfig

class RoofControl(metaclass=Singleton):

    def __init__(self):
        self.gpioconfig = GPIOConfig()

    def open(self):
        self.gpioconfig.turn_on(GPIOPin.SWITCH_ROOF)
        return self.gpioconfig.wait_for_falling(GPIOPin.VERIFY_OPEN)

    def close(self):
        self.gpioconfig.turn_off(GPIOPin.SWITCH_ROOF)
        return self.gpioconfig.wait_for_falling(GPIOPin.VERIFY_CLOSED)

    def read(self):
        is_roof_closed = self.gpioconfig.status(GPIOPin.VERIFY_CLOSED)
        is_roof_open = self.gpioconfig.status(GPIOPin.VERIFY_OPEN)
        is_switched_on = self.gpioconfig.status(GPIOPin.SWITCH_ROOF)

        if is_roof_closed and is_roof_open:
            raise TransitionError("""Roof state invalid - La chiusura del tetto è
            in uno stato invalido""")
        elif is_roof_closed and not is_switched_on:
            return RoofStatus.CLOSED
        elif is_roof_open and is_switched_on:
            return RoofStatus.OPEN
        elif is_switched_on:
            return RoofStatus.OPENING
        else:
            return RoofStatus.CLOSING
