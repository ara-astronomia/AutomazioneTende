import unittest
from unittest.mock import MagicMock
from curtains_control import WestCurtain, EastCurtain
from gpio_config import GPIOConfig
from gpio_pin import GPIOPin
from status import Status
from logger import Logger
from base.singleton import Singleton

class EastCurtainsTest(unittest.TestCase):

    def setUp(self):
        Singleton._instances = {}
        self.eastCurtain = EastCurtain()

    def test_open_curtain(self):
        GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.MOTORE_A or value == GPIOPin.MOTORE_E else False)
        self.assertEqual(Status.OPENING, self.eastCurtain.open())

    def test_close_curtain(self):
        GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.MOTORE_B or value == GPIOPin.MOTORE_E else False)
        self.assertEqual(Status.CLOSING, self.eastCurtain.close())

    def test_stop_curtains(self):
        GPIOConfig.status = MagicMock(return_value=False)
        self.assertEqual(Status.STOPPED, self.eastCurtain.stop())

class WestCurtainsTest(unittest.TestCase):

    def setUp(self):
        Singleton._instances = {}
        self.westCurtain = WestCurtain()

    def test_open_curtain(self):
        GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.MOTORW_A or value == GPIOPin.MOTORW_E else False)
        self.assertEqual(Status.OPENING, self.westCurtain.open())

    def test_close_curtain(self):
        GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.MOTORW_B or value == GPIOPin.MOTORW_E else False)
        self.assertEqual(Status.CLOSING, self.westCurtain.close())

    def test_stop_curtains(self):
        GPIOConfig.status = MagicMock(return_value=False)
        self.assertEqual(Status.STOPPED, self.westCurtain.stop())
