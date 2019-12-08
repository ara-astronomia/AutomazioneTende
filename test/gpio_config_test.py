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

    def test(self):
        gpioConfig = GPIOConfig()
        self.assertTrue(isinstance(gpioConfig, GPIOConfig))
        gpioConfig.turn_on(1)
        self.assertTrue(gpioConfig.wait_for_raising(1))
        self.assertFalse(gpioConfig.status(1))
