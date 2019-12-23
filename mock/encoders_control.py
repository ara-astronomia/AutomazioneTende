import config
from base.singleton import Singleton
from mock.curtains_control import EastCurtain, WestCurtain

class EncoderControl:
    def __init__(self):
        self.steps = 0
        self.__min_step__ = 0

    def move(self, step):
        self.steps = int(step)

class WestEncoder(EncoderControl, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.__max_step__ = config.Config.getInt("n_step_finecorsa", "encoder_step")
        self.motor = WestCurtain()

class EastEncoder(EncoderControl, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.__max_step__ = config.Config.getInt("n_step_finecorsa", "encoder_step")
        self.motor = EastCurtain()
