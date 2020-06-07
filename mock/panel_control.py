import config
from status import PanelStatus
from base.singleton import Singleton

class PanelControl(metaclass=Singleton):

    def __init__(self):
        self.is_on = PanelStatus.OFF

    def panel_on(self):
        self.is_on = PanelStatus.ON
        return self.is_on

    def panel_off(self):
        self.is_on = PanelStatus.OFF
        return self.is_on

    def read(self):
        return self.is_on
