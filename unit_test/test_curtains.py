import unittest
from curtains import Curtain
from unittest.mock import MagicMock, patch
from gpio_config import GPIOConfig
from gpio_pin import GPIOPin
from base.singleton import Singleton
from threading import Thread
import time
from status import CurtainsStatus
import config


def threaded_event_simulation(pin, pin_status, edge, callback, bouncetime=100):
    new_pin_status = GPIOConfig().status(pin)
    if pin_status != new_pin_status:
        if (edge == "BOTH" or
          (edge == "FALLING" and new_pin_status is False) or
          (edge == "RAISING" and new_pin_status is True)):
            callback(pin)
            pin_status = new_pin_status
    if bouncetime > 0:
        time.sleep(bouncetime/1000)
    return new_pin_status


class TestCurtain(unittest.TestCase):

    def east_curtain(self):
        return Curtain(clk=GPIOPin.CLK_E, dt=GPIOPin.DT_E, pin_verify_closed=GPIOPin.CURTAIN_E_VERIFY_CLOSED, pin_verify_open=GPIOPin.CURTAIN_E_VERIFY_OPEN, motor_a=GPIOPin.MOTORE_A, motor_b=GPIOPin.MOTORE_B, motor_e=GPIOPin.MOTORE_E)
    
    def west_curtain(self):
        return Curtain(clk=GPIOPin.CLK_W, dt=GPIOPin.DT_W, pin_verify_closed=GPIOPin.CURTAIN_W_VERIFY_CLOSED, pin_verify_open=GPIOPin.CURTAIN_W_VERIFY_OPEN, motor_a=GPIOPin.MOTORW_A, motor_b=GPIOPin.MOTORW_B, motor_e=GPIOPin.MOTORW_E)

    def setUp(self):
        Singleton._instances = {}

    def __reset_steps__(self, curtain, pin):

        """ It's like moving manually the curtain until it's all open or closed """

        curtain.__stop__ = MagicMock()

        curtain.gpioconfig.status = MagicMock(return_value=False)
        pin_status = curtain.gpioconfig.status(pin)
        pin_status = threaded_event_simulation(pin, pin_status, "RAISING", curtain.__reset_steps__)

        curtain.gpioconfig.status = MagicMock(side_effect=lambda value: True if value == pin else False)
        pin_status = threaded_event_simulation(pin, pin_status, "RAISING", curtain.__reset_steps__)

    def test_open_all_curtain(self):
        curtain = self.east_curtain()
        self.__reset_steps__(curtain, curtain.curtain_open)
        curtain.__stop__.assert_called_once()
        self.assertEqual(curtain.__max_step__, curtain.steps)

    def test_close_all_curtain(self):
        curtain = self.east_curtain()
        self.__reset_steps__(curtain, curtain.curtain_closed)
        curtain.__stop__.assert_called_once()
        self.assertEqual(curtain.__min_step__, curtain.steps)

    def __count_step__(self, curtain, step, forward=True):

        """
            It's like moving manually the curtain. The resolution can be improved.
        """

        statusA = True
        statusB = True
        if forward:
            pin = curtain.dt
        else:
            pin = curtain.clk

        def side_effect(value):
            if value == curtain.dt:
                return not statusA
            elif value == curtain.clk:
                return not statusB
            elif not curtain.is_opening and not curtain.is_closing and curtain.steps == curtain.__min_step__ and value == curtain.curtain_closed:
                return True
            elif not curtain.is_opening and not curtain.is_closing and curtain.steps == curtain.__max_step__ and value == curtain.curtain_open:
                return True
            else:
                return (
                            value == curtain.pin_enabling_motor or
                            (forward and value == curtain.pin_opening) or
                            (not forward and value == curtain.pin_closing)
                        )

        curtain.gpioconfig.status = MagicMock(side_effect=side_effect)

        for i in range(abs(step-curtain.steps)*4):
            if pin == curtain.dt:
                statusA = threaded_event_simulation(pin, statusA, "BOTH", curtain.__count_steps__)
                pin = curtain.clk
            else:
                statusB = threaded_event_simulation(pin, statusB, "BOTH", curtain.__count_steps__)
                pin = curtain.dt

        self.assertEqual(step, curtain.steps)

    def __count_steps_simple__(self, curtain, step, forward=True):

        """
            It's like moving manually the curtain. it has a better resolution
            than __count_steps__
        """

        statusA = True
        statusB = True
        pin = curtain.dt

        def side_effect(value):
            if value == curtain.dt:
                return not statusA
            elif value == curtain.clk:
                return not statusB
            elif not curtain.is_opening and not curtain.is_closing and curtain.steps == curtain.__min_step__ and value == curtain.curtain_closed:
                return True
            elif not curtain.is_opening and not curtain.is_closing and curtain.steps == curtain.__max_step__ and value == curtain.curtain_open:
                return True
            else:
                return (
                    value == curtain.pin_enabling_motor or
                    (forward and value == curtain.pin_opening) or
                    (not forward and value == curtain.pin_closing)
                )

        curtain.gpioconfig.status = MagicMock(side_effect=side_effect)

        for i in range(abs(step-curtain.steps)):
            statusA = threaded_event_simulation(pin, statusA, "BOTH", curtain.__count_steps_simple__)

        self.assertEqual(step, curtain.steps)

    def test_count_step_simple_east(self):
        curtain = self.east_curtain()
        self.__count_steps_simple__(curtain, 5)

    def test_count_step_simple_backwards_west(self):
        curtain = self.west_curtain()
        curtain.steps = 106
        self.__count_steps_simple__(curtain, 76, False)

    def test_count_step_east(self):
        curtain = self.east_curtain()
        self.__count_step__(curtain, 5)

    def test_count_step_west(self):
        curtain = self.west_curtain()
        self.__count_step__(curtain, 15)

    def test_count_step_backwards_east(self):
        curtain = self.east_curtain()
        curtain.steps = 100
        self.__count_step__(curtain, 95, False)

    def test_count_step_backwards_west(self):
        curtain = self.west_curtain()
        curtain.steps = 105
        self.__count_step__(curtain, 95, False)

    def __move__(self, curtain, status, final_steps, initial_steps=0):
        curtain.read = MagicMock(return_value=status)
        curtain.steps = initial_steps
        curtain.__close__ = MagicMock()
        curtain.__open__ = MagicMock()
        curtain.move(final_steps)
        curtain.read.assert_called_once()

    def test_west_should_open(self):
        curtain = self.west_curtain()
        self.__move__(curtain, CurtainsStatus.DISABLED, 5)
        curtain.__open__.assert_called_once()
        self.__move__(curtain, CurtainsStatus.STOPPED, 45, 23)
        curtain.__open__.assert_called_once()

    def test_east_should_close(self):
        curtain = self.east_curtain()
        self.__move__(curtain, CurtainsStatus.STOPPED, 7, 150)
        curtain.__close__.assert_called_once()
        self.__move__(curtain, CurtainsStatus.OPEN, 7, curtain.__max_step__)
        curtain.__close__.assert_called_once()

    def test_west_should_not_open_while_in_danger(self):
        curtain = self.west_curtain()
        self.__move__(curtain, CurtainsStatus.DANGER, 115)
        curtain.__close__.assert_not_called()
        curtain.__open__.assert_not_called()

    def test_east_should_not_open_while_moving(self):
        curtain = self.east_curtain()
        self.__move__(curtain, CurtainsStatus.OPENING, 115)
        curtain.__close__.assert_not_called()
        curtain.__open__.assert_not_called()

    def test_west_should_not_close_while_in_danger(self):
        curtain = self.west_curtain()
        self.__move__(curtain, CurtainsStatus.DANGER, 15, 96)
        curtain.__close__.assert_not_called()
        curtain.__open__.assert_not_called()

    def test_east_should_not_close_while_moving(self):
        curtain = self.east_curtain()
        self.__move__(curtain, CurtainsStatus.CLOSING, 73, 176)
        curtain.__close__.assert_not_called()
        curtain.__open__.assert_not_called()

    def test_read_is_danger(self):
        curtain = self.west_curtain()
        curtain.steps = curtain.__security_step__
        self.assertEqual(CurtainsStatus.DANGER, curtain.read())
        curtain.steps = curtain.__sub_min_step__
        self.assertEqual(CurtainsStatus.DANGER, curtain.read())

    def test_read_is_open(self):
        curtain = self.west_curtain()
        curtain.steps = curtain.__max_step__
        curtain.gpioconfig.status = MagicMock(side_effect=lambda value: True if value == curtain.curtain_open else False)
        self.assertEqual(CurtainsStatus.OPEN, curtain.read())

    def test_read_is_closed(self):
        curtain = self.west_curtain()
        curtain.gpioconfig.status = MagicMock(side_effect=lambda value: True if value == curtain.curtain_closed else False)
        self.assertEqual(CurtainsStatus.DISABLED, curtain.read())

    def test_read_is_stopped(self):
        curtain = self.west_curtain()
        curtain.steps = 10
        curtain.gpioconfig.status = MagicMock(return_value=False)
        self.assertEqual(CurtainsStatus.STOPPED, curtain.read())

    def test_read_is_error(self):
        curtain = self.west_curtain()
        curtain.gpioconfig.status = MagicMock(return_value=True)
        self.assertEqual(CurtainsStatus.ERROR, curtain.read())

    def test_open(self):
        curtain = self.east_curtain()
        curtain.gpioconfig.turn_on = MagicMock()
        curtain.gpioconfig.turn_off = MagicMock()
        curtain.__open__()
        curtain.gpioconfig.turn_on.assert_any_call(curtain.pin_opening)
        curtain.gpioconfig.turn_on.assert_called_with(curtain.pin_enabling_motor)
        curtain.gpioconfig.turn_off.assert_called_with(curtain.pin_closing)

    def test_close(self):
        curtain = self.east_curtain()
        curtain.gpioconfig.turn_on = MagicMock()
        curtain.gpioconfig.turn_off = MagicMock()
        curtain.__close__()
        curtain.gpioconfig.turn_off.assert_called_with(curtain.pin_opening)
        curtain.gpioconfig.turn_on.assert_called_with(curtain.pin_enabling_motor)
        curtain.gpioconfig.turn_on.assert_any_call(curtain.pin_closing)

    @patch('config.Config.getInt', MagicMock(return_value=1))
    def test_event_detect_1(self):
        curtain = self.west_curtain()
        curtain.gpioconfig.add_event_detect_both = MagicMock()
        curtain.gpioconfig.add_event_detect_on = MagicMock()
        curtain.__event_detect__()
        curtain.gpioconfig.add_event_detect_both.assert_called_once_with(curtain.dt, callback=curtain.__count_steps_simple__)
        curtain.gpioconfig.add_event_detect_on.assert_any_call(curtain.curtain_open, callback=curtain.__reset_steps__)
        curtain.gpioconfig.add_event_detect_on.assert_any_call(curtain.curtain_closed, callback=curtain.__reset_steps__)

    @patch('config.Config.getInt', MagicMock(return_value=0))
    def test_event_detect_0(self):
        curtain = self.west_curtain()
        curtain.gpioconfig.add_event_detect_both = MagicMock()
        curtain.gpioconfig.add_event_detect_on = MagicMock()
        curtain.__event_detect__()
        curtain.gpioconfig.add_event_detect_both.assert_any_call(curtain.dt, callback=curtain.__count_steps__)
        curtain.gpioconfig.add_event_detect_both.assert_any_call(curtain.clk, callback=curtain.__count_steps__)
        curtain.gpioconfig.add_event_detect_on.assert_any_call(curtain.curtain_open, callback=curtain.__reset_steps__)
        curtain.gpioconfig.add_event_detect_on.assert_any_call(curtain.curtain_closed, callback=curtain.__reset_steps__)

    def test_remove_event_detect(self):
        curtain = self.east_curtain()
        curtain.gpioconfig.remove_event_detect = MagicMock()
        curtain.__remove_event_detect__()
        curtain.gpioconfig.remove_event_detect.assert_any_call(curtain.dt)
        curtain.gpioconfig.remove_event_detect.assert_any_call(curtain.clk)
        curtain.gpioconfig.remove_event_detect.assert_any_call(curtain.curtain_open)
        curtain.gpioconfig.remove_event_detect.assert_any_call(curtain.curtain_closed)

    def test_open_up(self):
        curtain = self.east_curtain()
        curtain.move = MagicMock()
        curtain.open_up()
        curtain.move.assert_called_once_with(curtain.__max_step__)

    def test_bring_down(self):
        curtain = self.east_curtain()
        curtain.move = MagicMock()
        curtain.bring_down()
        curtain.move.assert_called_once_with(curtain.__min_step__)

    def __manual_reset__(self, curtain, status, pin, initial_steps):
        curtain.read = MagicMock(return_value=status)
        curtain.__stop__ = MagicMock()
        curtain.__open__ = MagicMock()
        curtain.__close__ = MagicMock()
        curtain.__remove_event_detect__ = MagicMock()
        curtain.__event_detect__ = MagicMock()
        curtain.gpioconfig.wait_for_on = MagicMock(return_value=pin)
        curtain.steps = initial_steps
        curtain.manual_reset()
        curtain.read.assert_called_once()
        if status == CurtainsStatus.STOPPED or status == CurtainsStatus.DANGER:
            curtain.__remove_event_detect__.assert_called_once()
            curtain.gpioconfig.wait_for_on.assert_called_once()
            curtain.__stop__.assert_called_once()
            curtain.__event_detect__.assert_called_once()
        else:
            curtain.__remove_event_detect__.assert_not_called()
            curtain.gpioconfig.wait_for_on.assert_not_called()
            curtain.__stop__.assert_not_called()
            curtain.__open__.assert_not_called()
            curtain.__close__.assert_not_called()
            curtain.__event_detect__.assert_not_called()
            self.assertEqual(initial_steps, curtain.steps)

    def test_manual_reset_to_closed(self):
        curtain = self.west_curtain()
        self.__manual_reset__(curtain, CurtainsStatus.STOPPED, curtain.curtain_closed, 10)
        curtain.__close__.assert_called_once()
        self.assertEqual(curtain.__min_step__, curtain.steps)

    def test_manual_reset_to_closed_not_working(self):
        curtain = self.west_curtain()
        self.__manual_reset__(curtain, CurtainsStatus.STOPPED, None, 10)
        curtain.__close__.assert_called_once()
        self.assertEqual(curtain.__sub_min_step__, curtain.steps)

    def test_manual_reset_to_open(self):
        curtain = self.east_curtain()
        self.__manual_reset__(curtain, CurtainsStatus.STOPPED, curtain.curtain_open, curtain.__max_step__ - 25)
        curtain.__open__.assert_called_once()
        self.assertEqual(curtain.__max_step__, curtain.steps)

    def test_manual_reset_to_open_not_working(self):
        curtain = self.east_curtain()
        self.__manual_reset__(curtain, CurtainsStatus.STOPPED, None, curtain.__max_step__ - 5)
        curtain.__open__.assert_called_once()
        self.assertEqual(curtain.__security_step__, curtain.steps)

    def test_manual_reset_fails_when_opening(self):
        curtain = self.west_curtain()
        self.__manual_reset__(curtain, CurtainsStatus.OPENING, curtain.curtain_open, curtain.__max_step__ - 15)

if __name__ == '__main__':
    unittest.main()
