import config
from base.singleton import Singleton
from gpio_pin import GPIOPin
from curtains_control import EastCurtain, WestCurtain
from gpio_config import GPIOConfig
import threading
from status import Status
from transition_error import TransitionError

# method to force reset steps when in danger
# method to (re)calibrate the steps

class EncoderControl:
    def __init__(self):
        self.__min_step__ = 0
        self.steps = 0
        self.__max_step__ = config.Config.getInt("n_step_corsa", "encoder_step")
        self.__security_step__ = config.Config.getInt("n_step_sicurezza", "encoder_step")
        self.target = None
        self.gpioconfig = GPIOConfig()
        if config.Config.getInt("count_steps_simple", "encoder_step") == 0:
            self.gpioconfig.add_event_detect_both(self.dt, callback=self.__count_steps__)
            self.gpioconfig.add_event_detect_both(self.clk, callback=self.__count_steps__)
        else:
            self.gpioconfig.add_event_detect_both(self.dt, callback=self.__count_steps_simple__)
        self.gpioconfig.add_event_detect_on(self.curtain_open, callback=self.__reset_steps__)
        self.gpioconfig.add_event_detect_on(self.curtain_closed, callback=self.__reset_steps__)
        self.switch_a = False
        self.switch_b = False
        self.lockRotary = threading.Lock()

    def __open__(self):
        self.gpioconfig.turn_on(self.pin_opening)
        self.gpioconfig.turn_off(self.pin_closing)
        self.gpioconfig.turn_on(self.pin_enabling_motor)

    def __close__(self):
        self.gpioconfig.turn_off(self.pin_opening)
        self.gpioconfig.turn_on(self.pin_closing)
        self.gpioconfig.turn_on(self.pin_enabling_motor)

    def __stop__(self):
        self.gpioconfig.turn_off(self.pin_opening)
        self.gpioconfig.turn_off(self.pin_closing)
        self.gpioconfig.turn_off(self.pin_enabling_motor)

    def __count_steps__(self, dt_or_clk):
        self.switch_a = self.gpioconfig.status(self.dt)
        self.switch_b = self.gpioconfig.status(self.clk)
        if self.switch_a and self.switch_b:
            self.lockRotary.acquire()
            if dt_or_clk == self.clk and self.read() == Status.CLOSING:
                self.steps -= 1
            elif dt_or_clk == self.dt and self.read() == Status.OPENING:
                self.steps += 1
            if self.steps == self.target or self.target == None or self.steps == self.__security_step__:
                self.target = None
                self.__stop__()
            if self.steps < self.__min_step__:
                self.steps = self.__min_step__
            self.lockRotary.release()

    def __count_steps_simple__(self, dt):
        self.lockRotary.acquire()
        if self.read() == Status.CLOSING:
            self.steps -= 1
        elif self.read() == Status.OPENING:
            self.steps += 1
        if self.steps == self.target or self.target == None or self.steps >= self.__security_step__:
            self.target = None
            self.__stop__()
        self.lockRotary.release()

    def __reset_steps__(self, dt_or_clk):
        self.lockRotary.acquire()
        self.__stop__()
        try:
            if dt_or_clk == self.curtain_open:
                self.steps = self.__max_step__
            elif dt_or_clk == self.curtain_closed:
                self.steps = self.__min_step__
            else:
                raise TransitionError("""Curtain state invalid - La tenda è
                in uno stato invalido""")
        finally:
            self.lockRotary.release()

    def read(self):
        self.is_opening = self.gpioconfig.status(self.pin_opening)
        self.is_closing = self.gpioconfig.status(self.pin_closing)
        self.is_enable = self.gpioconfig.status(self.pin_enabling_motor)
        self.is_open = self.gpioconfig.status(self.curtain_open)
        self.is_closed = self.gpioconfig.status(self.curtain_closed)
        if self.steps >= self.__max_step__ or self.steps < self.__min_step__:
            return Status.DANGER
        elif self.is_opening and self.is_enable and not self.is_closing and not self.is_open and not self.is_closed:
            return Status.OPENING
        elif self.is_enable and self.is_closing and not self.is_opening and not self.is_open and not self.is_closed:
            return Status.CLOSING
        elif self.is_open and not self.is_enable:
            return Status.OPEN
        elif self.is_closed and not self.is_enable:
            return Status.CLOSED
        elif not self.is_enable:
            return Status.STOPPED
        else:
            raise TransitionError("""Curtain state invalid - La tenda è
            in uno stato invalido""")

    def move(self, step):
        self.target = int(step)

        # while the motors are moving we don't want to start another movement
        if (self.read() > Status.OPEN):
            return

        # deciding the movement direction
        if self.steps < self.target:
            self.__open__()
        if self.steps > self.target:
            self.__close__()

class WestEncoder(EncoderControl, metaclass=Singleton):
    def __init__(self):
        self.clk = GPIOPin.CLK_W
        self.dt = GPIOPin.DT_W
        self.curtain_closed = GPIOPin.CURTAIN_W_VERIFY_CLOSED
        self.curtain_open = GPIOPin.CURTAIN_W_VERIFY_OPEN
        self.pin_opening = GPIOPin.MOTORW_A
        self.pin_closing = GPIOPin.MOTORW_B
        self.pin_enabling_motor = GPIOPin.MOTORW_E
        super().__init__()

class EastEncoder(EncoderControl, metaclass=Singleton):
    def __init__(self):
        self.clk = GPIOPin.CLK_E
        self.dt = GPIOPin.DT_E
        self.curtain_closed = GPIOPin.CURTAIN_E_VERIFY_CLOSED
        self.curtain_open = GPIOPin.CURTAIN_E_VERIFY_OPEN
        self.pin_opening = GPIOPin.MOTORE_A
        self.pin_closing = GPIOPin.MOTORE_B
        self.pin_enabling_motor = GPIOPin.MOTORE_E
        super().__init__()
