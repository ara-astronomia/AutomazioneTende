from gpio_pin import GPIOPin
from status import Orientation
from gpiozero import RotaryEncoder
from config import Config


class BuilderCurtain:

    def __init__(self) -> None:
        self._clk = None
        self._dt = None
        self._rotary_encoder = None
        self._pin_verify_closed = None
        self._pin_verify_open = None
        self._motor_a = None
        self._motor_b = None
        self._motor_e = None

    @property
    def rotary_encoder(self):
        return self._rotary_encoder

    @rotary_encoder.setter
    def rotary_encoder(self, rotary_encoder):
        self._rotary_encoder = rotary_encoder

    @property
    def pin_verify_closed(self):
        return self._pin_verify_closed

    @pin_verify_closed.setter
    def pin_verify_closed(self, pin_verify_closed):
        self._pin_verify_closed = pin_verify_closed

    @property
    def pin_verify_open(self):
        return self._pin_verify_open

    @pin_verify_open.setter
    def pin_verify_open(self, pin_verify_open):
        self._pin_verify_open = pin_verify_open

    @property
    def motor_a(self):
        return self._motor_a

    @motor_a.setter
    def motor_a(self, motor_a):
        self._motor_a = motor_a

    @property
    def motor_b(self):
        return self._motor_b

    @motor_b.setter
    def motor_b(self, motor_b):
        self._motor_b = motor_b

    @property
    def motor_e(self):
        return self._motor_e

    @motor_e.setter
    def motor_e(self, motor_e):
        self._motor_e = motor_e

    def build(self):
        from components.curtains.curtains import Curtain
        return Curtain(self.rotary_encoder, self.pin_verify_closed, self.pin_verify_open, self.motor_a, self.motor_b, self.motor_e)


class FactoryCurtain:

    @staticmethod
    def curtain(orientation: Orientation, mock=False):
        if mock:
            from mock.curtains import Curtain
            return Curtain()

        if orientation is Orientation.EAST:
            builder_curtain = BuilderCurtain()
            builder_curtain.pin_verify_closed = GPIOPin.CURTAIN_E_VERIFY_CLOSED
            builder_curtain.pin_verify_open = GPIOPin.CURTAIN_E_VERIFY_OPEN
            builder_curtain.motor_a = GPIOPin.MOTORE_A
            builder_curtain.motor_b = GPIOPin.MOTORE_B
            builder_curtain.motor_e = GPIOPin.MOTORE_E
            builder_curtain.rotary_encoder = RotaryEncoder(
                Config.getInt("clk_e", "encoder_board"),
                Config.getInt("dt_e", "encoder_board"),
                max_steps=Config.getInt("n_step_corsa", "encoder_step")
            )
            curtain = builder_curtain.build()

        elif orientation is Orientation.WEST:
            builder_curtain = BuilderCurtain()
            builder_curtain.pin_verify_closed = GPIOPin.CURTAIN_W_VERIFY_CLOSED
            builder_curtain.pin_verify_open = GPIOPin.CURTAIN_W_VERIFY_OPEN
            builder_curtain.motor_a = GPIOPin.MOTORW_A
            builder_curtain.motor_b = GPIOPin.MOTORW_B
            builder_curtain.motor_e = GPIOPin.MOTORW_E
            builder_curtain.rotary_encoder = RotaryEncoder(
                Config.getInt("clk_w", "encoder_board"),
                Config.getInt("dt_w", "encoder_board"),
                max_steps=Config.getInt("n_step_corsa", "encoder_step")
            )
            curtain = builder_curtain.build()
        else:
            raise ValueError("Orientation invalid")

        return curtain
