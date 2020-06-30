from status import ButtonStatus
from gpio_config import GPIOConfig


class ButtonControl():
    def __init__(self, pin):
        self.pin = pin
        self.gpioconfig = GPIOConfig()

    def on(self):
        self.gpioconfig.turn_on(self.pin)

    def off(self):
        self.gpioconfig.turn_off(self.pin)

    def read(self):
        if self.gpioconfig.status(self.pin):
            return ButtonStatus.ON
        else:
            return ButtonStatus.OFF
