from gpiozero import OutputDevice

from status import ButtonStatus


class ButtonControl():
    def __init__(self, pin):
        self.output = OutputDevice(pin)

    def on(self):
        self.output.on()

    def off(self):
        self.output.off()

    def read(self):
        if self.output.value:
            return ButtonStatus.ON
        else:
            return ButtonStatus.OFF
