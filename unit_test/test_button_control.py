import unittest

from gpiozero import Device
from gpiozero import OutputDevice
from gpiozero.pins.mock import MockFactory
from unittest.mock import MagicMock, patch

from components.button_control import ButtonControl
from config import Config
from status import ButtonStatus


class TestButtonControl(unittest.TestCase):
    def setUp(self):
        if Device.pin_factory is not None:
            Device.pin_factory.reset()

        Device.pin_factory = MockFactory()

    def panel_control(self):
        return ButtonControl(Config.getInt("switch_panel", "panel_board"))

    def power_tele_control(self):
        return ButtonControl(Config.getInt("switch_power", "panel_board"))

    def light_control(self):
        return ButtonControl(Config.getInt("switch_light", "panel_board"))

    def power_ccd_control(self):
        return ButtonControl(Config.getInt("switch_aux", "panel_board"))

    def test_panel_control(self):
        self.__check_button__(self.panel_control())

    def test_power_tele_control(self):
        self.__check_button__(self.power_tele_control())

    def test_light_control(self):
        self.__check_button__(self.light_control())

    def test_power_ccd_control(self):
        self.__check_button__(self.power_ccd_control())

    def __check_button__(self, button):
        with patch.object(OutputDevice, 'on', return_value=None) as mock_method:
            button.on()
            mock_method.assert_called_once()
        with patch.object(OutputDevice, 'off', return_value=None) as mock_method:
            button.off()
            mock_method.assert_called_once()

    def test_read_button(self):
        button = self.panel_control()
        button.on()
        self.assertEqual(button.read(), ButtonStatus.ON)
        button.off()
        self.assertEqual(button.read(), ButtonStatus.OFF)
