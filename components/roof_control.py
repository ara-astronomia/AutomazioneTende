from gpiozero import OutputDevice, Button

from config import Config
from logger import Logger
from status import Status


class RoofControl():

    def __init__(self):
        self.motor = OutputDevice(Config.getInt("switch_roof_open", "roof_board"))
        self.roof_closed_switch = Button(Config.getInt("roof_verify_closed", "roof_board"), pull_up=True)
        self.roof_open_switch = Button(Config.getInt("roof_verify_open", "roof_board"), pull_up=True)

    def open(self):
        self.motor.on()
        return self.roof_open_switch.wait_for_press()

    def close(self):
        self.motor.off()
        return self.roof_closed_switch.wait_for_press()

    def read(self):
        is_roof_closed = self.roof_closed_switch.is_pressed
        is_roof_open = self.roof_open_switch.is_pressed
        is_switched_on = self.motor.value

        if is_roof_closed and is_roof_open:
            return Status.ERROR
        elif is_roof_closed and not is_switched_on:
            return Status.CLOSED
        elif is_roof_open and is_switched_on:
            return Status.OPEN
        elif is_switched_on:
            return Status.OPENING
        else:
            return Status.CLOSING
