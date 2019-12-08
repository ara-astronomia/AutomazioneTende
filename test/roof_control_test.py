import unittest
from unittest.mock import patch, MagicMock
from transition_error import TransitionError

MockRPi = MagicMock()
modules = {
    "RPi": MockRPi,
    "RPi.GPIO": MockRPi.GPIO,
}
patcher = patch.dict("sys.modules", modules)
patcher.start()
from roof_control import RoofControl
from gpio_config import GPIOConfig

class RoofControlTest(unittest.TestCase):
    def setUp(self):
        self.roofControl = RoofControl(GPIOConfig())

    def test_is_instance(self):
        self.assertTrue(isinstance(self.roofControl, RoofControl))

    def test_open_roof(self):
        self.roofControl.open()

    def test_close_roof(self):
        self.roofControl.close()

    def test_raises_error_when_is_open_and_closed(self):
        status = MagicMock(return_value=True)
        GPIOConfig.status = status
        with self.assertRaises(TransitionError):
            self.roofControl.read()

#    def test_is_roof_closed(self):
