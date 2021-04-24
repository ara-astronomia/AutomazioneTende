from threading import Thread
from time import sleep

from components.roof_control import RoofControl


class MockRoofControl(RoofControl):

    def __init__(self):
        super().__init__()
        self.roof_open_switch.pin.drive_high()
        self.roof_closed_switch.pin.drive_low()

    def open(self):
        self.roof_open_switch.pin.drive_high()
        self.roof_closed_switch.pin.drive_high()
        t = Thread(target=self.__wait_for_open__, args=(self.roof_open_switch.pin,))
        t.start()
        super().open()
        t.join()
        return True

    def close(self):
        self.roof_open_switch.pin.drive_high()
        self.roof_closed_switch.pin.drive_high()
        t = Thread(target=self.__wait_for_open__, args=(self.roof_closed_switch.pin,))
        t.start()
        super().close()
        t.join()
        return True

    def __wait_for_open__(self, pin):
        sleep(10)
        pin.drive_low()
