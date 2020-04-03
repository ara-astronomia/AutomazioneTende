import config
from base.singleton import Singleton
from gpio_pin import GPIOPin
from gpio_config import GPIOConfig
import threading
from status import Status

class Curtain:
    def __init__(self):
        self.__sub_min_step__ = -5
        self.__min_step__ = 0
        self.steps = 0
        self.__max_step__ = config.Config.getInt("n_step_corsa", "encoder_step")
        self.__security_step__ = config.Config.getInt("n_step_sicurezza", "encoder_step")
        self.target = None
        self.gpioconfig = GPIOConfig()
        self.encoder_a = False
        self.encoder_b = False
        self.lockRotary = threading.Lock()
        self.is_opening = False
        self.is_closing = False
        self.is_enable = False
        self.is_open = False
        self.is_closed = False
        self.dt = None
        self.clk = None
        self.curtain_open = None
        self.curtain_closed = None
        self.pin_opening = None
        self.pin_closing = None
        self.pin_enabling_motor = None

    def __event_detect__(self):
        if config.Config.getInt("count_steps_simple", "encoder_step") == 0:
            self.gpioconfig.add_event_detect_both(self.dt, callback=self.__count_steps__)
            self.gpioconfig.add_event_detect_both(self.clk, callback=self.__count_steps__)
        else:
            self.gpioconfig.add_event_detect_both(self.dt, callback=self.__count_steps_simple__)
        self.gpioconfig.add_event_detect_on(self.curtain_open, callback=self.__reset_steps__)
        self.gpioconfig.add_event_detect_on(self.curtain_closed, callback=self.__reset_steps__)

    def __remove_event_detect__(self):
        self.gpioconfig.remove_event_detect(self.dt)
        self.gpioconfig.remove_event_detect(self.clk)
        self.gpioconfig.remove_event_detect(self.curtain_open)
        self.gpioconfig.remove_event_detect(self.curtain_closed)

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
        finally:
            self.lockRotary.release()

    def manual_reset(self):

        """ Reset the steps counter with the help of the edge switchers """

        status = self.read()
        if status != Status.STOPPED and status != Status.DANGER:
            return
        self.__remove_event_detect__()

        distance_to_min_step = abs(self.steps - self.__min_step__)
        distance_to_max_step = abs(self.__max_step__ - self.steps)

        if distance_to_min_step <= distance_to_max_step:
            self.__close__()
            pin = self.gpioconfig.wait_for_on(self.curtain_closed)
            self.__stop__()
            if pin:
                self.steps = self.__min_step__
            else:
                self.steps = self.__sub_min_step__
        else:
            self.__open__()
            pin = self.gpioconfig.wait_for_on(self.curtain_open)
            self.__stop__()
            if pin:
                self.steps = self.__max_step__
            else:
                self.steps = self.__security_step__

        self.__event_detect__()

    def read(self):

        """ Read the status of the curtain based on the pin of motor, encoder and switches """

        self.is_opening = self.gpioconfig.status(self.pin_opening)
        self.is_closing = self.gpioconfig.status(self.pin_closing)
        self.is_enable = self.gpioconfig.status(self.pin_enabling_motor)
        self.is_open = self.gpioconfig.status(self.curtain_open)
        self.is_closed = self.gpioconfig.status(self.curtain_closed)

        status = None
        if (
            self.steps > self.__max_step__ or self.steps < self.__min_step__ or
            (self.steps == self.__max_step__ and not self.is_open and not self.is_closing) or
            (self.steps == self.__min_step__ and not self.is_closed and not self.is_opening)
        ):
            status = Status.DANGER
        elif self.is_opening and self.is_enable and not self.is_closing and not self.is_open and not self.is_closed:
            status = Status.OPENING
        elif self.is_enable and self.is_closing and not self.is_opening and not self.is_open and not self.is_closed:
            status = Status.CLOSING
        elif self.is_open and not self.is_enable:
            status = Status.OPEN
        elif self.is_closed and not self.is_enable:
            status = Status.CLOSED
        elif not self.is_enable:
            status = Status.STOPPED

        if not status:
            status = Status.ERROR

        return status

    def move(self, step):

        """ Move the motor in a direction based on the starting and target steps """

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

        """
            Open up the curtain completely
            It's a shortcut to move()
        """

        self.move(self.__max_step__)

    def bring_down(self):

        """
            Bring down the curtain completely
            It's a shortcut to move()
        """

        self.move(self.__min_step__)

    def motor_stop(self):

        """
            disable pin motor
        """

        self.__stop__()



class WestCurtain(Curtain, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.clk = GPIOPin.CLK_W
        self.dt = GPIOPin.DT_W
        self.curtain_closed = GPIOPin.CURTAIN_W_VERIFY_CLOSED
        self.curtain_open = GPIOPin.CURTAIN_W_VERIFY_OPEN
        self.pin_opening = GPIOPin.MOTORW_A
        self.pin_closing = GPIOPin.MOTORW_B
        self.pin_enabling_motor = GPIOPin.MOTORW_E
        self.__event_detect__()

class EastCurtain(Curtain, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.clk = GPIOPin.CLK_E
        self.dt = GPIOPin.DT_E
        self.curtain_closed = GPIOPin.CURTAIN_E_VERIFY_CLOSED
        self.curtain_open = GPIOPin.CURTAIN_E_VERIFY_OPEN
        self.pin_opening = GPIOPin.MOTORE_A
        self.pin_closing = GPIOPin.MOTORE_B
        self.pin_enabling_motor = GPIOPin.MOTORE_E
        self.__event_detect__()
