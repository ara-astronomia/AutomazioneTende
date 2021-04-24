import unittest
from unittest.mock import patch
from components.roof_control import RoofControl
from gpiozero import Device, OutputDevice, Button
from gpiozero.pins.mock import MockFactory
from status import Status
from base.singleton import Singleton


class RoofControlTest(unittest.TestCase):
    def setUp(self):
        if Device.pin_factory is not None:
            Device.pin_factory.reset()

        Device.pin_factory = MockFactory()

        Singleton._instances = {}
        self.roofControl = RoofControl()

    def test_open_roof(self):
        with patch.object(self.roofControl.roof_open_switch, 'wait_for_press', return_value=True) as mockedroofopen:
            with patch.object(self.roofControl.roof_closed_switch, 'wait_for_press', return_value=True) as mockedroofclosed:
                self.roofControl.open()
                mockedroofopen.assert_called_once()
                mockedroofclosed.assert_not_called()

    def test_open_roof(self):
        with patch.object(self.roofControl.roof_open_switch, 'wait_for_press', return_value=True) as mockedroofopen:
            with patch.object(self.roofControl.roof_closed_switch, 'wait_for_press', return_value=True) as mockedroofclosed:
                self.roofControl.close()
                mockedroofclosed.assert_called_once()
                mockedroofopen.assert_not_called()

    def test_raises_error_when_is_open_and_closed(self):
        self.roofControl.roof_closed_switch.pin.drive_low()
        self.roofControl.roof_open_switch.pin.drive_low()
        self.assertEqual(Status.ERROR, self.roofControl.read())

    def test_is_roof_closed(self):
        self.roofControl.motor.off()
        self.roofControl.roof_closed_switch.pin.drive_low()
        self.roofControl.roof_open_switch.pin.drive_high()
        self.assertEqual(Status.CLOSED, self.roofControl.read())

    def test_is_roof_open(self):
        self.roofControl.motor.on()
        self.roofControl.roof_closed_switch.pin.drive_high()
        self.roofControl.roof_open_switch.pin.drive_low()
        self.assertEqual(Status.OPEN, self.roofControl.read())

    def test_is_roof_in_opening(self):
        self.roofControl.motor.on()
        self.roofControl.roof_closed_switch.pin.drive_high()
        self.roofControl.roof_open_switch.pin.drive_high()
        self.assertEqual(Status.OPENING, self.roofControl.read())

    def test_is_roof_begin_opening(self):
        self.roofControl.motor.on()
        self.roofControl.roof_closed_switch.pin.drive_low()
        self.roofControl.roof_open_switch.pin.drive_high()
        self.assertEqual(Status.OPENING, self.roofControl.read())

    def test_is_roof_in_closing(self):
        self.roofControl.motor.off()
        self.roofControl.roof_closed_switch.pin.drive_high()
        self.roofControl.roof_open_switch.pin.drive_high()
        self.assertEqual(Status.CLOSING, self.roofControl.read())

    def test_is_roof_begin_closing(self):
        self.roofControl.motor.off()
        self.roofControl.roof_closed_switch.pin.drive_high()
        self.roofControl.roof_open_switch.pin.drive_low()
        self.assertEqual(Status.CLOSING, self.roofControl.read())
