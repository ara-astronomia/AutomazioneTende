from components.curtains.curtains import Curtain
from logger import Logger


class MockCurtain(Curtain):

    def __init__(self, rotary_encoder, curtain_closed, curtain_open, motor):
        super().__init__(rotary_encoder, curtain_closed, curtain_open, motor)

    def __rotate_cw__(self, *inputs):
        [input.pin.drive_low() for input in inputs if self.target is not None]
        [input.pin.drive_high() for input in inputs if self.target is not None]

    def __rotate_ccw__(self, *inputs):
        [input.pin.drive_low() for input in reversed(inputs) if self.target is not None]
        [input.pin.drive_high() for input in reversed(inputs) if self.target is not None]

    def __check_curtains_limit__(self):
        if self.steps() <= self.__min_step__:
            self.curtain_closed.pin.drive_low()
        else:
            self.curtain_closed.pin.drive_high()
        if self.steps() >= self.__max_step__:
            self.curtain_open.pin.drive_low()
        else:
            self.curtain_open.pin.drive_high()

    def __open__(self):
        super().__open__()
        while self.motor.is_active:
            self.__rotate_cw__(self.rotary_encoder.a, self.rotary_encoder.b)
            self.__check_curtains_limit__()

    def __close__(self):
        super().__close__()
        while self.motor.is_active:
            self.__rotate_ccw__(self.rotary_encoder.a, self.rotary_encoder.b)
            self.__check_curtains_limit__()
