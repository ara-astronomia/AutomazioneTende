import unittest
from unittest.mock import patch, MagicMock

MockRPi = MagicMock()
modules = {
    "RPi": MockRPi,
    "RPi.GPIO": MockRPi.GPIO,
}
patcher = patch.dict("sys.modules", modules)
patcher.start()

from gpio_config import GPIOConfig

class GPIOConfigTest(unittest.TestCase):
    def setUp(self):
        self.gpioConfig = GPIOConfig()

    def test_is_instance(self):
        self.assertTrue(isinstance(self.gpioConfig, GPIOConfig))

    def test_generic_exec(self):
        self.gpioConfig.turn_on(1)
        self.gpioConfig.turn_off(1)
        self.assertTrue(self.gpioConfig.wait_for_raising(1))
        self.assertTrue(self.gpioConfig.wait_for_falling(1))
        self.assertFalse(self.gpioConfig.status(1))

    def test_is_singleton(self):
        self.assertEqual(GPIOConfig(), self.gpioConfig)
