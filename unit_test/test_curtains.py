import unittest

from gpiozero import Device
from gpiozero.input_devices import RotaryEncoder
from gpiozero.pins.mock import MockFactory
from unittest.mock import MagicMock, patch

from components.curtains.factory_curtain import FactoryCurtain
from status import CurtainsStatus, Orientation


class TestCurtain(unittest.TestCase):

    def setUp(self):
        if Device.pin_factory is not None:
            Device.pin_factory.reset()

        Device.pin_factory = MockFactory()

    def east_curtain(self):
        return FactoryCurtain.curtain(orientation=Orientation.EAST, mock=True)

    def west_curtain(self):
        return FactoryCurtain.curtain(orientation=Orientation.WEST, mock=True)

    def test_when_rotated_cw(self):
        # given
        curtain = self.west_curtain()
        curtain.target = 1

        with patch.object(RotaryEncoder, 'when_rotated', return_value=None) as mock_method:
            # when
            curtain.__rotate_cw__(curtain.rotary_encoder.a, curtain.rotary_encoder.b)

            # then
            mock_method.assert_any_call()

    def test_when_rotated_ccw(self):
        # given
        curtain = self.west_curtain()
        curtain.rotary_encoder.steps = 10
        curtain.target = 1

        with patch.object(RotaryEncoder, 'when_rotated', return_value=None) as mock_method:
            # when
            curtain.__rotate_ccw__(curtain.rotary_encoder.a, curtain.rotary_encoder.b)

            # then
            mock_method.assert_any_call()

    def test_curtain_is_closed(self):
        # given
        curtain = self.west_curtain()
        curtain.is_disabled = False

        # when
        curtain.curtain_closed.pin.drive_low()
        curtain.curtain_open.pin.drive_high()

        # then
        self.assertEqual(curtain.read(), CurtainsStatus.CLOSED)

    def test_curtain_is_open(self):
        # given
        curtain = self.west_curtain()
        curtain.is_disabled = False

        # when
        curtain.curtain_closed.pin.drive_high()
        curtain.curtain_open.pin.drive_low()

        # then
        self.assertEqual(curtain.read(), CurtainsStatus.OPEN)

    def test_open_all_curtain(self):
        # given
        curtain = self.west_curtain()
        curtain.is_disabled = False
        curtain.curtain_closed.pin.drive_low()
        self.assertEqual(curtain.__min_step__, curtain.steps())
        self.assertEqual(curtain.read(), CurtainsStatus.CLOSED)

        # when
        curtain.open_up()

        # then
        self.assertEqual(curtain.__max_step__, curtain.steps())
        self.assertEqual(curtain.read(), CurtainsStatus.OPEN)

    def test_close_all_curtain(self):
        # given
        curtain = self.east_curtain()
        curtain.is_disabled = False
        curtain.curtain_open.pin.drive_low()
        curtain.rotary_encoder.steps = curtain.__max_step__
        self.assertEqual(curtain.read(), CurtainsStatus.OPEN)

        # when
        curtain.bring_down()

        # then
        self.assertEqual(curtain.__min_step__, curtain.steps())
        self.assertEqual(curtain.read(), CurtainsStatus.CLOSED)

    def test_increase_step_east(self):
        # given
        final_step = 5
        curtain = self.east_curtain()

        # when
        curtain.move(final_step)

        # then
        self.assertEqual(final_step, curtain.steps())

    def test_decrease_step_west(self):
        # given
        initial_step = 106
        final_step = 101
        curtain = self.west_curtain()
        curtain.rotary_encoder.steps = initial_step

        # when
        curtain.move(final_step)

        # then
        self.assertEqual(final_step, curtain.steps())

    def test_west_should_open(self):
        # given
        curtain = self.west_curtain()
        curtain.__open__ = MagicMock()
        curtain.read = MagicMock(return_value=CurtainsStatus.STOPPED)

        # when
        curtain.move(5)

        # then
        curtain.__open__.assert_called_once()
        curtain.read.assert_called_once()

    def test_east_should_close(self):
        # given
        curtain = self.east_curtain()
        curtain.__close__ = MagicMock()
        curtain.read = MagicMock(return_value=CurtainsStatus.STOPPED)
        curtain.rotary_encoder.steps = 80

        # when
        curtain.move(75)

        # then
        curtain.__close__.assert_called_once()
        curtain.read.assert_called_once()

    def test_west_should_not_open_while_in_danger(self):
        # given
        curtain = self.west_curtain()
        curtain.read = MagicMock(return_value=CurtainsStatus.DANGER)
        curtain.__close__ = MagicMock()
        curtain.__open__ = MagicMock()

        # when
        curtain.move(75)

        # then
        curtain.__close__.assert_not_called()
        curtain.__open__.assert_not_called()

    def test_east_should_not_open_while_moving(self):
        # given
        curtain = self.east_curtain()
        curtain.read = MagicMock(return_value=CurtainsStatus.OPENING)
        curtain.__close__ = MagicMock()
        curtain.__open__ = MagicMock()

        # when
        curtain.move(75)

        # then
        curtain.__close__.assert_not_called()
        curtain.__open__.assert_not_called()

    def test_in_security_step_status_is_danger(self):
        # given
        curtain = self.west_curtain()

        # when
        curtain.rotary_encoder.steps = curtain.__security_step__

        # then
        self.assertEqual(CurtainsStatus.DANGER, curtain.read())

        # when
        curtain.rotary_encoder.steps = curtain.__sub_min_step__

        # then
        self.assertEqual(CurtainsStatus.DANGER, curtain.read())

    def test_in_curtain_opened_status_is_open(self):
        # given
        curtain = self.west_curtain()
        curtain.rotary_encoder.steps = curtain.__max_step__
        curtain.curtain_open.pin.drive_low()
        curtain.curtain_closed.pin.drive_high()

        # then
        self.assertEqual(CurtainsStatus.OPEN, curtain.read())

    def test_in_curtain_closed_status_is_closed(self):
        # given
        curtain = self.west_curtain()
        curtain.rotary_encoder.steps = curtain.__min_step__
        curtain.is_disabled = False
        curtain.curtain_closed.pin.drive_low()
        curtain.curtain_open.pin.drive_high()

        # then
        self.assertEqual(CurtainsStatus.CLOSED, curtain.read())

    def test_when_curtain_not_opened_neither_closed_status_is_stopped(self):
        # given
        curtain = self.west_curtain()
        curtain.is_disabled = False
        curtain.rotary_encoder.steps = 10
        curtain.curtain_closed.pin.drive_high()
        curtain.curtain_open.pin.drive_high()

        # then
        self.assertEqual(CurtainsStatus.STOPPED, curtain.read())

    def test_when_curtain_both_opened_and_closed_status_is_error(self):
        # given
        curtain = self.west_curtain()
        curtain.is_disabled = False
        curtain.curtain_closed.pin.drive_low()
        curtain.curtain_open.pin.drive_low()

        # then
        self.assertEqual(CurtainsStatus.ERROR, curtain.read())

    # can't test manual reset with this curtain implementation
    # def test_manual_reset_to_closed(self):
    #     # given
    #     curtain = self.west_curtain()
    #     curtain.rotary_encoder.steps = -3
    #     curtain.curtain_closed.pin.drive_high()
    #     curtain.curtain_open.pin.drive_high()

    #     # when
    #     curtain.manual_reset()

    #     # then
    #     self.assertEqual(curtain.__min_step__, curtain.steps)


if __name__ == '__main__':
    unittest.main()
