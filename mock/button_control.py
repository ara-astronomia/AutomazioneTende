from status import ButtonStatus


class ButtonControl():
    def __init__(self, pin):
        self.status = False
        self.pin = pin

    def on(self):
        self.status = True

    def off(self):
        self.status = False

    def read(self):
        if self.status:
            return ButtonStatus.ON
        else:
            return ButtonStatus.OFF
