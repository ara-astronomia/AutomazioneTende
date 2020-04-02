import config
from base.singleton import Singleton
import threading
from status import Status

class Curtain:
    def __init__(self):
        self.__sub_min_step__ = -5
        self.__min_step__ = 0
        self.steps = 0
        self.__max_step__ = config.Config.getInt("n_step_corsa", "encoder_step")
        self.__security_step__ = config.Config.getInt("n_step_sicurezza", "encoder_step")
        self.lockRotary = threading.Lock()

    def manual_reset(self):

        """ Reset the steps counter with the help of the edge switchers """

        status = self.read()
        if status != Status.STOPPED and status != Status.DANGER:
            return

        distance_to_min_step = abs(self.steps - self.__min_step__)
        distance_to_max_step = abs(self.__max_step__ - self.steps)

        if distance_to_min_step <= distance_to_max_step:
            self.steps = self.__min_step__
        else:
            self.steps = self.__max_step__

    def read(self):

        """ Read the status of the curtain based on the pin of motor, encoder and switches """

        status = None

        if self.steps == self.__max_step__:
            status = Status.OPEN
        elif self.steps == self.__min_step__:
            status = Status.CLOSED
        else:
            status = Status.STOPPED

        if not status:
            status = Status.ERROR

        return status

    def move(self, step):

        """ Move the motor in a direction based on the starting and target steps """

        self.steps = step

    def open_up(self):

        """
            Open up the curtain completely
            It's a shortcut to move()
        """

        self.steps = self.__max_step__

    def bring_down(self):

        """
            Bring down the curtain completely
            It's a shortcut to move()
        """

        self.steps = self.__min_step__

    def stop_motor(self):

        """
            disable pin motor
        """
        print ("inserire qui il metodo che mette il pin dei motori in disable")
        pass

class WestCurtain(Curtain, metaclass=Singleton):
    def __init__(self):
        super().__init__()

class EastCurtain(Curtain, metaclass=Singleton):
    def __init__(self):
        super().__init__()
