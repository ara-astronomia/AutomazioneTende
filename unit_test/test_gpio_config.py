import config, unittest
from unittest.mock import patch, MagicMock
from base.singleton import Singleton
from gpio_config import GPIOConfig
from gpio_pin import GPIOPin
import configparser

class GPIOConfigTest(unittest.TestCase):
    def setUp(self):
        Singleton._instances = {}
        self.gpioConfig = GPIOConfig()

    def test_is_instance(self):
        self.assertTrue(isinstance(self.gpioConfig, GPIOConfig))

    def test_generic_exec(self):
        GPIOConfig.status = MagicMock(side_effect=lambda value: value != GPIOPin.SWITCH_ROOF)
        GPIOConfig.wait_for_off = MagicMock(return_value = True)
        GPIOConfig.wait_for_on = MagicMock(return_value = True)
        self.gpioConfig.turn_on(GPIOPin.SWITCH_ROOF)
        self.gpioConfig.turn_off(GPIOPin.SWITCH_ROOF)
        self.assertTrue(self.gpioConfig.wait_for_on(GPIOPin.SWITCH_ROOF))
        self.assertTrue(self.gpioConfig.wait_for_off(GPIOPin.SWITCH_ROOF))
        self.assertFalse(self.gpioConfig.status(GPIOPin.SWITCH_ROOF))

    def test_is_singleton(self):
        self.assertEqual(GPIOConfig(), self.gpioConfig)

    def test_timeout_value(self):
        cparser = configparser.ConfigParser()
        cparser.read('config.ini')
        self.assertEqual(config.Config.getInt("wait_for_timeout", "roof_board"), cparser["roof_board"].getint("wait_for_timeout"))
        self.assertEqual(config.Config.getInt("event_bouncetime", "roof_board"), cparser["roof_board"].getint("event_bouncetime"))
