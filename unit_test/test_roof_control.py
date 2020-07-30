import unittest
from unittest.mock import MagicMock
from components.roof_control import RoofControl
from gpio_config import GPIOConfig
from gpio_pin import GPIOPin
from status import Status
from base.singleton import Singleton


class RoofControlTest(unittest.TestCase):
    def setUp(self):
        Singleton._instances = {}
        self.roofControl = RoofControl()

    def test_is_instance(self):
        self.assertTrue(isinstance(self.roofControl, RoofControl))

    def test_open_roof(self):
        self.roofControl.open()

    def test_close_roof(self):
        self.roofControl.close()

    def test_raises_error_when_is_open_and_closed(self):
        status = MagicMock(return_value=True)
        GPIOConfig.status = status
        self.assertEqual(Status.ERROR, self.roofControl.read())

    def test_is_roof_closed(self):
        side_effect = lambda value: True if value == GPIOPin.VERIFY_CLOSED else False
        status = MagicMock(side_effect=side_effect)
        GPIOConfig.status = status
        self.assertEqual(Status.CLOSED, self.roofControl.read())

    def test_is_roof_open(self):
        side_effect = lambda value: False if value == GPIOPin.VERIFY_CLOSED else True
        status = MagicMock(side_effect=side_effect)
        GPIOConfig.status = status
        self.assertEqual(Status.OPEN, self.roofControl.read())

    def test_is_roof_in_opening(self):
        side_effect = lambda value: True if value == GPIOPin.SWITCH_ROOF else False
        status = MagicMock(side_effect=side_effect)
        GPIOConfig.status = status
        self.assertEqual(Status.OPENING, self.roofControl.read())

    def test_is_roof_in_closing(self):
        status = MagicMock(return_value=False)
        GPIOConfig.status = status
        self.assertEqual(Status.CLOSING, self.roofControl.read())
