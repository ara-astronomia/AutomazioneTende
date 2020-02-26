from status import Status
from base.singleton import Singleton
from logger import Logger

class CurtainControl:

    def __init__(self):
        self.is_open = Status.STOPPED

    def open(self):
        self.is_open = Status.OPENING
        return self.is_open

    def close(self):
        self.is_open = Status.CLOSING
        return self.is_open

    def stop(self):
        self.is_open = Status.STOPPED
        return self.is_open

    def read(self):
        return self.is_open

class EastCurtain(CurtainControl, metaclass=Singleton):

    def __init__(self):
        super().__init__()

class WestCurtain(CurtainControl, metaclass=Singleton):

    def __init__(self):
        super().__init__()
