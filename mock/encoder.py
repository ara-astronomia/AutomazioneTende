import config
from time import sleep
from base.base_encoder import BaseEncoder

class Encoder(BaseEncoder):
    def __init__(self, orientation: "E or W", max_step):
        self.current_step = 0
        self.__motion_step__ = 0
        self.__min_step__ = 0
        self.__max_step__ = max_step
        # TODO set the GPIO pin based on orientation
        self.orientation = orientation

    def __save_current_step__(self, direction):
        """
            solo questo metodo andrebbe implementato diversamente nella classe che comunica con l'encoder reale:
            si dovrebbe lusare RPi.GPIO per andare a leggere l'hardware e aggiornare di conseguenza il valore degli step
        """
        if direction == "F":
            self.__motion_step__ = self.__motion_step__ + 1
        elif direction == "B":
            self.__motion_step__ = self.__motion_step__ - 1
        sleep(config.Config.getFloat("sleep"))
