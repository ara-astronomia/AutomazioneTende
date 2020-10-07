import unittest
from unittest.mock import MagicMock, patch
from components.button_control import ButtonControl
from gpio_config import GPIOConfig
from gpio_pin import GPIOPin
from base.singleton import Singleton
from status import ButtonStatus
import time
import config


class TestButtonControl(unittest.TestCase):

    def panel_control(self):
        return ButtonControl(GPIOPin.SWITCH_PANEL)

    def power_tele_control(self):
        return ButtonControl(GPIOPin.SWITCH_POWER)

    def light_control(self):
        return ButtonControl(GPIOPin.SWITCH_LIGHT)

    def power_ccd_control(self):
        return ButtonControl(GPIOPin.SWITCH_AUX)

    def setUp(self):
        Singleton._instances = {}

    def test_panel_control(self):
        self.__check_button__(self.panel_control())

    def test_power_tele_control(self):
        self.__check_button__(self.power_tele_control())

    def test_light_control(self):
        self.__check_button__(self.light_control())

    def test_power_ccd_control(self):
        self.__check_button__(self.power_ccd_control())

    def __check_button__(self, button):
        button.gpioconfig = MagicMock()
        button.on()
        button.gpioconfig.turn_on.assert_called_once()
        button.off()
        button.gpioconfig.turn_off.assert_called_once()

    def test_read_button(self):
        button = self.panel_control()
        button.gpioconfig.status = MagicMock(return_value=True)
        self.assertEqual(button.read(), ButtonStatus.ON)
        button.gpioconfig.status = MagicMock(return_value=False)
        self.assertEqual(button.read(), ButtonStatus.OFF)
