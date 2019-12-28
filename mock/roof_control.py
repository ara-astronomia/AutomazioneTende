import config
from status import Status
from base.singleton import Singleton

class RoofControl(metaclass=Singleton):

    def __init__(self):
        self.is_open = Status.CLOSED

    def open(self):
        self.is_open = Status.OPEN
        return self.is_open

    def close(self):
        self.is_open = Status.CLOSED
        return self.is_open

    def read(self):
        return self.is_open
