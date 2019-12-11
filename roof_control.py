import config
from time import sleep
from status import Status
from transition_error import TransitionError
from gpio_pin import GPIOPin

class RoofControl:

    def __init__(self, gpioconfig):
        self.gpioconfig = gpioconfig

    def open(self):
        self.gpioconfig.turn_on(GPIOPin.SWITCH_ROOF)
        return self.gpioconfig.wait_for_falling(GPIOPin.VERIFY_OPEN)

    def close(self):
        self.gpioconfig.turn_off(GPIOPin.SWITCH_ROOF)
        return self.gpioconfig.wait_for_falling(GPIOPin.VERIFY_CLOSED)

    def read(self):
        is_roof_closed = self.gpioconfig.status(GPIOPin.VERIFY_CLOSED)
        is_roof_open = self.gpioconfig.status(GPIOPin.VERIFY_OPEN)
        if is_roof_closed and is_roof_open:
            raise TransitionError("""Roof state invalid - La chiusura del tetto è
            in uno stato invalido""")
        elif is_roof_closed:
            return Status.CLOSED
        elif is_roof_open:
            return Status.OPEN
        else:
            return Status.TRANSIT
