import unittest
from unittest.mock import patch, MagicMock

from gpio_config import GPIOConfig
from gpio_pin import GPIOPin

class GPIOConfigTest(unittest.TestCase):
    def setUp(self):
        self.gpioConfig = GPIOConfig()

    def test_is_instance(self):
        self.assertTrue(isinstance(self.gpioConfig, GPIOConfig))

    def test_generic_exec(self):
        self.gpioConfig.turn_on(GPIOPin.SWITCH_ROOF)
        self.gpioConfig.turn_off(GPIOPin.SWITCH_ROOF)
        self.assertTrue(self.gpioConfig.wait_for_raising(GPIOPin.SWITCH_ROOF))
        self.assertTrue(self.gpioConfig.wait_for_falling(GPIOPin.SWITCH_ROOF))
        self.assertFalse(self.gpioConfig.status(GPIOPin.SWITCH_ROOF))

    def test_is_singleton(self):
        self.assertEqual(GPIOConfig(), self.gpioConfig)
