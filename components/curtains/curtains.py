import config
from gpio_config import GPIOConfig
from status import CurtainsStatus


class Curtain:
    def __init__(self, rotary_encoder, pin_verify_closed, pin_verify_open, motor_a, motor_b, motor_e):
        self.__sub_min_step__ = -5
        self.__min_step__ = 0
        self.__max_step__ = config.Config.getInt("n_step_corsa", "encoder_step")
        self.__security_step__ = config.Config.getInt("n_step_sicurezza", "encoder_step")
        self.target = None
        self.gpioconfig = GPIOConfig()
        self.encoder_a = False
        self.encoder_b = False
        self.is_opening = False
        self.is_closing = False
        self.is_enable = False
        self.is_open = False
        self.is_closed = False
        self.rotary_encoder = rotary_encoder
        self.is_disabled = True

        self.curtain_closed = pin_verify_closed
        self.curtain_open = pin_verify_open
        self.pin_opening = motor_a
        self.pin_closing = motor_b
        self.pin_enabling_motor = motor_e
        self.__event_detect__()

    def __event_detect__(self):
        self.gpioconfig.add_event_detect_on(self.curtain_open, callback=self.__reset_steps__)
        self.gpioconfig.add_event_detect_on(self.curtain_closed, callback=self.__reset_steps__)
        self.rotary_encoder.when_rotated(self.__check_and_stop__)

    def __remove_event_detect__(self):
        self.rotary_encoder.when_rotated(None)
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
        self.gpioconfig.turn_off(self.pin_enabling_motor)
        self.gpioconfig.turn_off(self.pin_opening)
        self.gpioconfig.turn_off(self.pin_closing)

    def __check_and_stop__(self):
        if (
            self.steps() == self.target or
            self.target is None or
            self.steps() >= self.__security_step__ or
            self.steps() <= self.__sub_min_step__
        ):
            self.__stop__()
            self.target = None

    def __reset_steps__(self, open_or_closed):
        self.__stop__()

        if open_or_closed == self.curtain_open:
            self.rotary_encoder.steps = self.__max_step__
        elif open_or_closed == self.curtain_closed:
            self.rotary_encoder.steps = self.__min_step__

    def manual_reset(self):

        """ Reset the steps counter with the help of the edge switchers """

        status = self.read()
        if status != CurtainsStatus.STOPPED and status != CurtainsStatus.DANGER:
            return
        self.__remove_event_detect__()

        distance_to_min_step = abs(self.steps() - self.__min_step__)
        distance_to_max_step = abs(self.__max_step__ - self.steps())

        if distance_to_min_step <= distance_to_max_step:
            self.__close__()
            pin = self.gpioconfig.wait_for_on(self.curtain_closed)
            self.__stop__()
            if pin:
                self.rotary_encoder.steps = self.__min_step__
            else:
                self.rotary_encoder.steps = self.__sub_min_step__
        else:
            self.__open__()
            pin = self.gpioconfig.wait_for_on(self.curtain_open)
            self.__stop__()
            if pin:
                self.rotary_encoder.steps = self.__max_step__
            else:
                self.rotary_encoder.steps = self.__security_step__

        self.__event_detect__()

    def steps(self):
        return self.rotary_encoder.steps

    def read(self):

        """ Read the status of the curtain based on the pin of motor, encoder and switches """

        self.is_opening = self.gpioconfig.status(self.pin_opening)
        self.is_closing = self.gpioconfig.status(self.pin_closing)
        self.is_enable = self.gpioconfig.status(self.pin_enabling_motor)
        self.is_open = self.gpioconfig.status(self.curtain_open)
        self.is_closed = self.gpioconfig.status(self.curtain_closed)

        status = None
        if (
            self.steps() > self.__max_step__ or self.steps() < self.__min_step__ or
            (self.steps() == self.__max_step__ and not self.is_open and not self.is_closing) or
            (self.steps() == self.__min_step__ and not self.is_closed and not self.is_opening)
        ):
            status = CurtainsStatus.DANGER
        elif self.is_opening and self.is_enable and not self.is_closing and not self.is_open and not self.is_closed:
            status = CurtainsStatus.OPENING
        elif self.is_enable and self.is_closing and not self.is_opening and not self.is_open and not self.is_closed:
            status = CurtainsStatus.CLOSING
        elif self.is_open and not self.is_enable:
            status = CurtainsStatus.OPEN
        elif self.is_closed and not self.is_enable and self.is_disabled:
            status = CurtainsStatus.DISABLED
        elif self.is_closed and not self.is_enable:
            status = CurtainsStatus.CLOSED
        elif not self.is_enable:
            status = CurtainsStatus.STOPPED

        if not status:
            status = CurtainsStatus.ERROR

        return status

    def move(self, step):

        """ Move the motor in a direction based on the starting and target steps """

        # while the motors are moving we don't want to start another movement
        if (self.read() > CurtainsStatus.OPEN):
            return

        self.target = step

        # deciding the movement direction
        if self.steps() < self.target:
            self.__open__()
        if self.steps() > self.target:
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
