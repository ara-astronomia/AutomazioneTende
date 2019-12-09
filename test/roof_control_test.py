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
from gpio_pin import GPIOPin
from status import Status

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

    def test_is_roof_in_transition(self):
        status = MagicMock(return_value=False)
        GPIOConfig.status = status
        self.assertEqual(Status.TRANSIT, self.roofControl.read())
