import unittest
from curtains import WestCurtain, EastCurtain
from unittest.mock import MagicMock
from gpio_config import GPIOConfig
from gpio_pin import GPIOPin
from base.singleton import Singleton
from threading import Thread
import time
from status import Status

def threaded_event_simulation(pin, pin_status, edge, callback, bouncetime=100):
    new_pin_status = GPIOConfig().status(pin)
    if pin_status != new_pin_status:
        if (edge == "BOTH" or
          (edge == "FALLING" and new_pin_status == False) or
          (edge == "RAISING" and new_pin_status == True)):
            callback(pin)
            pin_status = new_pin_status
    if bouncetime > 0:
        time.sleep(bouncetime/1000)
    return new_pin_status

class TestCurtain(unittest.TestCase):

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
        curtain = EastCurtain()
        self.__reset_steps__(curtain, curtain.curtain_open)
        curtain.__stop__.assert_called_once()
        self.assertEqual(curtain.__max_step__, curtain.steps)

    def test_close_all_curtain(self):
        curtain = EastCurtain()
        self.__reset_steps__(curtain, curtain.curtain_closed)
        curtain.__stop__.assert_called_once()
        self.assertEqual(curtain.__min_step__, curtain.steps)

    def __count_step__(self, curtain, step, forward=True):

        """ It's like moving manually the curtain """

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
            else:
                return (value == curtain.pin_enabling_motor or
                        (forward and value == curtain.pin_opening) or
                        not forward and value == curtain.pin_closing)

        curtain.gpioconfig.status = MagicMock(side_effect=side_effect)

        for i in range(abs(step-curtain.steps)*4):
            if pin == curtain.dt:
                statusA = threaded_event_simulation(pin, statusA, "BOTH", curtain.__count_steps__)
                pin = curtain.clk
            else:
                statusB = threaded_event_simulation(pin, statusB, "BOTH", curtain.__count_steps__)
                pin = curtain.dt

        self.assertEqual(step, curtain.steps)

    def test_count_step_east(self):
        curtain = EastCurtain()
        self.__count_step__(curtain, 5)

    def test_count_step_west(self):
        curtain = WestCurtain()
        self.__count_step__(curtain, 15)

    def test_count_step_backwards_east(self):
        curtain = EastCurtain()
        curtain.steps = 100
        self.__count_step__(curtain, 95, False)

    def test_count_step_backwards_west(self):
        curtain = WestCurtain()
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
        curtain = WestCurtain()
        self.__move__(curtain, Status.CLOSED, 5)
        curtain.__open__.assert_called_once()
        self.__move__(curtain, Status.STOPPED, 45, 23)
        curtain.__open__.assert_called_once()

    def test_east_should_open(self):
        curtain = EastCurtain()
        self.__move__(curtain, Status.CLOSED, 9)
        curtain.__open__.assert_called_once()
        self.__move__(curtain, Status.STOPPED, 57, 32)
        curtain.__open__.assert_called_once()

    def test_east_should_close(self):
        curtain = EastCurtain()
        self.__move__(curtain, Status.STOPPED, 7, 150)
        curtain.__close__.assert_called_once()
        self.__move__(curtain, Status.OPEN, 7, curtain.__max_step__)
        curtain.__close__.assert_called_once()

    def test_west_close(self):
        curtain = WestCurtain()
        self.__move__(curtain, Status.STOPPED, 5, 165)
        curtain.__close__.assert_called_once()
        self.__move__(curtain, Status.OPEN, 0, curtain.__max_step__)
        curtain.__close__.assert_called_once()

    def test_east_should_not_open_while_moving(self):
        curtain = EastCurtain()
        self.__move__(curtain, Status.OPENING, 115)
        curtain.__close__.assert_not_called()
        curtain.__open__.assert_not_called()

    def test_west_should_not_open_while_moving(self):
        curtain = WestCurtain()
        self.__move__(curtain, Status.OPENING, 115)
        curtain.__close__.assert_not_called()
        curtain.__open__.assert_not_called()

    def test_east_should_not_close_while_moving(self):
        curtain = EastCurtain()
        self.__move__(curtain, Status.CLOSING, 73, 176)
        curtain.__close__.assert_not_called()
        curtain.__open__.assert_not_called()

    def test_west_should_not_close_while_moving(self):
        curtain = WestCurtain()
        self.__move__(curtain, Status.CLOSING, 73, 176)
        curtain.__close__.assert_not_called()
        curtain.__open__.assert_not_called()

if __name__ == '__main__':
    unittest.main()
