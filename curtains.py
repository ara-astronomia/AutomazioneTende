import config
from base.singleton import Singleton
from gpio_pin import GPIOPin
from curtains_control import EastCurtain, WestCurtain
from gpio_config import GPIOConfig
import threading
from status import Status
from transition_error import TransitionError

class Curtain:
    def __init__(self):
        self.__sub_min_step__ = -5
        self.__min_step__ = 0
        self.steps = 0
        self.__max_step__ = config.Config.getInt("n_step_corsa", "encoder_step")
        self.__security_step__ = config.Config.getInt("n_step_sicurezza", "encoder_step")
        self.target = None
        self.gpioconfig = GPIOConfig()
        self.__event_detect__()
        self.encoder_a = False
        self.encoder_b = False
        self.lockRotary = threading.Lock()

    def __event_detect__(self):
        if config.Config.getInt("count_steps_simple", "encoder_step") == 0:
            self.gpioconfig.add_event_detect_both(self.dt, callback=self.__count_steps__)
            self.gpioconfig.add_event_detect_both(self.clk, callback=self.__count_steps__)
        else:
            self.gpioconfig.add_event_detect_both(self.dt, callback=self.__count_steps_simple__)
        self.gpioconfig.add_event_detect_on(self.curtain_open, callback=self.__reset_steps__)
        self.gpioconfig.add_event_detect_on(self.curtain_closed, callback=self.__reset_steps__)

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

    def __check_and_stop__(self, status):
        if (status != Status.CLOSING and status != Status.OPENING and
          (self.steps == self.target and self.__min_step__ < self.target < self.__max_step__) or
          self.target == None or
          self.steps >= self.__security_step__ or
          self.steps <= self.__sub_min_step__):
            self.__stop__()
            self.target = None

    def __count_steps__(self, dt_or_clk):
        self.encoder_a = self.gpioconfig.status(self.dt)
        self.encoder_b = self.gpioconfig.status(self.clk)
        if self.encoder_a and self.encoder_b:
            self.lockRotary.acquire()
            try:
                status = self.read()
                if dt_or_clk == self.clk and status == Status.CLOSING:
                    self.steps -= 1
                elif dt_or_clk == self.dt and status == Status.OPENING:
                    self.steps += 1
                self.__check_and_stop__(status)
            finally:
                self.lockRotary.release()

    def __count_steps_simple__(self, dt):
        self.lockRotary.acquire()
        try:
            status = self.read()
            if status == Status.CLOSING:
                self.steps -= 1
            elif status == Status.OPENING:
                self.steps += 1
            self.__check_and_stop__(status)
        finally:
            self.lockRotary.release()

    def __reset_steps__(self, open_or_closed):
        self.lockRotary.acquire()
        self.__stop__()
        try:
            if open_or_closed == self.curtain_open:
                self.steps = self.__max_step__
            elif open_or_closed == self.curtain_closed:
                self.steps = self.__min_step__
            else:
                raise TransitionError("""Curtain state invalid - La tenda è
                in uno stato invalido""")
        finally:
            self.lockRotary.release()

    def manual_reset(self):
        status = self.read()
        if status != Status.STOPPED and status != Status.DANGER:
            return

        self.gpioconfig.remove_event_detect(self.dt)
        self.gpioconfig.remove_event_detect(self.clk)
        self.gpioconfig.remove_event_detect(self.curtain_open)
        self.gpioconfig.remove_event_detect(self.curtain_closed)

        if abs(self.steps - self.__min_step__) <= abs(self.__max_step__ - self.steps):
            self.__close__()
            pin = self.gpioconfig.wait_for_on(self.curtain_closed)
            self.__stop__()
            if pin is None:
                self.steps = self.__sub_min_step__
            self.steps = self.__min_step__
        else:
            self.__open__()
            self.gpioconfig.wait_for_on(self.curtain_open)
            self.__stop__()
            if pin is None:
                self.steps = self.__security_step__
            self.steps = self.__max_step__

        self.__event_detect__()

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
        # while the motors are moving we don't want to start another movement
        if (self.read() > Status.OPEN):
            return

        self.target = int(step)

        # deciding the movement direction
        if self.steps < self.target:
            self.__open__()
        if self.steps > self.target:
            self.__close__()

    def open_up(self):
        self.move(self.__max_step__)

    def bring_down(self):
        self.move(self.__min_step__)

class WestCurtain(Curtain, metaclass=Singleton):
    def __init__(self):
        self.clk = GPIOPin.CLK_W
        self.dt = GPIOPin.DT_W
        self.curtain_closed = GPIOPin.CURTAIN_W_VERIFY_CLOSED
        self.curtain_open = GPIOPin.CURTAIN_W_VERIFY_OPEN
        self.pin_opening = GPIOPin.MOTORW_A
        self.pin_closing = GPIOPin.MOTORW_B
        self.pin_enabling_motor = GPIOPin.MOTORW_E
        super().__init__()

class EastCurtain(Curtain, metaclass=Singleton):
    def __init__(self):
        self.clk = GPIOPin.CLK_E
        self.dt = GPIOPin.DT_E
        self.curtain_closed = GPIOPin.CURTAIN_E_VERIFY_CLOSED
        self.curtain_open = GPIOPin.CURTAIN_E_VERIFY_OPEN
        self.pin_opening = GPIOPin.MOTORE_A
        self.pin_closing = GPIOPin.MOTORE_B
        self.pin_enabling_motor = GPIOPin.MOTORE_E
        super().__init__()
