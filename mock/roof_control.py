import config
from status import RoofStatus
from base.singleton import Singleton

class RoofControl(metaclass=Singleton):

    def __init__(self):
        self.is_open = RoofStatus.CLOSED

    def open(self):
        self.is_open = RoofStatus.OPEN
        return self.is_open

    def close(self):
        self.is_open = RoofStatus.CLOSED
        return self.is_open

    def read(self):
        return self.is_open
