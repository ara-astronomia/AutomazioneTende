import unittest
from unittest.mock import patch
from components.roof_control import RoofControl
from mock.roof_control import MockRoofControl
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from status import Status
from base.singleton import Singleton


class RoofControlTest(unittest.TestCase):
    def setUp(self):
        if Device.pin_factory is not None:
            Device.pin_factory.reset()

        Device.pin_factory = MockFactory()

        Singleton._instances = {}

    def getRoofControl(self):
        return RoofControl()

    def getMockRoofControl(self):
        return MockRoofControl()

    def test_open_roof(self):
        roofControl = self.getRoofControl()
        with patch.object(roofControl.roof_open_switch, 'wait_for_press', return_value=True) as mockedroofopen:
            with patch.object(roofControl.roof_closed_switch, 'wait_for_press', return_value=True) as mockedroofclosed:
                roofControl.open()
                mockedroofopen.assert_called_once()
                mockedroofclosed.assert_not_called()

    def test_open_roof(self):
        roofControl = self.getRoofControl()
        with patch.object(roofControl.roof_open_switch, 'wait_for_press', return_value=True) as mockedroofopen:
            with patch.object(roofControl.roof_closed_switch, 'wait_for_press', return_value=True) as mockedroofclosed:
                roofControl.close()
                mockedroofclosed.assert_called_once()
                mockedroofopen.assert_not_called()

    def test_raises_error_when_is_open_and_closed(self):
        roofControl = self.getRoofControl()
        roofControl.roof_closed_switch.pin.drive_low()
        roofControl.roof_open_switch.pin.drive_low()
        self.assertEqual(Status.ERROR, roofControl.read())

    def test_is_roof_closed(self):
        roofControl = self.getMockRoofControl()
        roofControl.close()
        self.assertEqual(Status.CLOSED, roofControl.read())

    def test_is_roof_open(self):
        roofControl = self.getMockRoofControl()
        roofControl.open()
        self.assertEqual(Status.OPEN, roofControl.read())

    def test_is_roof_in_opening(self):
        roofControl = self.getRoofControl()
        roofControl.motor.on()
        roofControl.roof_closed_switch.pin.drive_high()
        roofControl.roof_open_switch.pin.drive_high()
        self.assertEqual(Status.OPENING, roofControl.read())

    def test_is_roof_begin_opening(self):
        roofControl = self.getRoofControl()
        roofControl.motor.on()
        roofControl.roof_closed_switch.pin.drive_low()
        roofControl.roof_open_switch.pin.drive_high()
        self.assertEqual(Status.OPENING, roofControl.read())

    def test_is_roof_in_closing(self):
        roofControl = self.getRoofControl()
        roofControl.motor.off()
        roofControl.roof_closed_switch.pin.drive_high()
        roofControl.roof_open_switch.pin.drive_high()
        self.assertEqual(Status.CLOSING, roofControl.read())

    def test_is_roof_begin_closing(self):
        roofControl = self.getRoofControl()
        roofControl.motor.off()
        roofControl.roof_closed_switch.pin.drive_high()
        roofControl.roof_open_switch.pin.drive_low()
        self.assertEqual(Status.CLOSING, roofControl.read())
