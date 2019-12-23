from status import CurtainStatus
from base.singleton import Singleton
from logger import Logger

class CurtainControl:

    def __init__(self, gpioconfig):
        self.gpioconfig = gpioconfig
        self.is_open = CurtainStatus.STOPPED

    def open(self):
        self.is_open = CurtainStatus.OPENING
        return self.is_open

    def close(self):
        self.is_open = CurtainStatus.CLOSING
        return self.is_open

    def stop(self):
        self.is_open = CurtainStatus.STOPPED
        return self.is_open

    def read(self):
        return self.is_open

class EastCurtain(CurtainControl, metaclass=Singleton):

    def __init__(self, gpioconfig):
        super().__init__(gpioconfig)

class WestCurtain(CurtainControl, metaclass=Singleton):

    def __init__(self, gpioconfig):
        super().__init__(gpioconfig)
