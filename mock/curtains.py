import config
from base.singleton import Singleton
import threading
from status import CurtainsStatus


class Curtain:
    def __init__(self):
        self.__sub_min_step__ = -5
        self.__min_step__ = 0
        self._steps = 0
        self.__max_step__ = config.Config.getInt("n_step_corsa", "encoder_step")
        self.__security_step__ = config.Config.getInt("n_step_sicurezza", "encoder_step")
        self.lockRotary = threading.Lock()
        self.is_disabled = True

    def manual_reset(self):

        """ Reset the steps counter with the help of the edge switchers """

        status = self.read()
        if status != CurtainsStatus.STOPPED and status != CurtainsStatus.DANGER:
            return

        distance_to_min_step = abs(self._steps - self.__min_step__)
        distance_to_max_step = abs(self.__max_step__ - self._steps)

        if distance_to_min_step <= distance_to_max_step:
            self._steps = self.__min_step__
        else:
            self._steps = self.__max_step__

    def read(self):

        """ Read the status of the curtain based on the pin of motor, encoder and switches """

        status = None

        if self._steps == self.__max_step__:
            status = CurtainsStatus.OPEN
        elif self._steps == self.__min_step__ and self.is_disabled is True:
            status = CurtainsStatus.DISABLED
        elif self._steps == self.__min_step__:
            status = CurtainsStatus.CLOSED
        else:
            status = CurtainsStatus.STOPPED

        if not status:
            status = CurtainsStatus.ERROR

        return status

    def move(self, step):

        """ Move the motor in a direction based on the starting and target steps """

        self._steps = step

    def open_up(self):

        """
            Open up the curtain completely
            It's a shortcut to move()
        """

        self._steps = self.__max_step__

    def bring_down(self):

        """
            Bring down the curtain completely
            It's a shortcut to move()
        """

        self._steps = self.__min_step__

    def motor_stop(self):

        """ Disable pin motor """

        status = None
        status = CurtainsStatus.STOPPED
        return status

    def steps(self):
        return self._steps
