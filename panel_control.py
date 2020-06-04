import config
from time import sleep
from status import PanelStatus
from gpio_pin import GPIOPin
from base.singleton import Singleton
from gpio_config import GPIOConfig

class PanelControl(metaclass=Singleton):

    def __init__(self):
        self.gpioconfig = GPIOConfig()

    def panel_on(self):
        self.gpioconfig.turn_on(GPIOPin.SWITCH_PANEL)
        #return self.gpioconfig.wait_for_off(GPIOPin.VERIFY_OPEN)

    def panel_off(self):
        self.gpioconfig.turn_off(GPIOPin.SWITCH_PANEL)
        #return self.gpioconfig.wait_for_off(GPIOPin.VERIFY_CLOSED)

     def read(read):
         is_panel_on = self.gpioconfig.status(GPIOPin.SWITCH_PANEL)
         #is_switched_on = self.gpioconfig.status(GPIOPin.SWITCH_ROOF)

         if is_panel_on:
             return PanelStatus.ON
         else:
             return PanelStatus.OFF
