import unittest
from curtains import WestCurtain, EastCurtain
from unittest.mock import MagicMock
from gpio_config import GPIOConfig
from gpio_pin import GPIOPin
from base.singleton import Singleton
from threading import Thread
import time

def thread_function(pin, pin_status, edge, callback, bouncetime=100):
    new_pin_status = GPIOConfig().status(pin)
    if pin_status != new_pin_status:
        if (edge == "BOTH" or
          (edge == "FALLING" and new_pin_status == False) or
          (edge == "RAISING" and new_pin_status == True)):
            callback(pin)
            pin_status = new_pin_status
    if bouncetime > 0:
        time.sleep(bouncetime/1000)

class EncoderTest(unittest.TestCase):

    def setUp(self):
        Singleton._instances = {}
#        GPIOConfig.add_event_detect_both = MagicMock()
#        GPIOConfig.add_event_detect_raising = MagicMock()

    def count_step(self, encoder, step, forward=True):

        """ It's like moving manually the encoder """

        statusA = True
        statusB = True
        if forward:
            pin = encoder.dt
        else:
            pin = encoder.clk

        def side_effect(value):
            if value == encoder.dt:
                return not statusA
            elif value == encoder.clk:
                return not statusB
            else:
                return (value == encoder.pin_enabling_motor or
                        (forward and value == encoder.pin_opening) or
                        not forward and value == encoder.pin_closing)

        encoder.gpioconfig.status = MagicMock(side_effect=side_effect)

        for i in range(abs(step-encoder.steps)*4):
            if pin == encoder.dt:
                thread_function(pin, statusA, "BOTH", encoder.__count_steps__)
                statusA = not statusA
                pin = encoder.clk
            else:
                thread_function(pin, statusB, "BOTH", encoder.__count_steps__)
                statusB = not statusB
                pin = encoder.dt

        self.assertEqual(step, encoder.steps)

    def test_count_step_east(self):
        encoder = EastCurtain()
        self.count_step(encoder, 5)

    def test_count_step_west(self):
        encoder = WestCurtain()
        self.count_step(encoder, 15)

    def test_count_step_backwards_east(self):
        encoder = EastCurtain()
        encoder.steps = 100
        self.count_step(encoder, 95, False)

    def test_count_step_backwards_west(self):
        encoder = WestCurtain()
        encoder.steps = 105
        self.count_step(encoder, 95, False)

    # def test_west_open(self):
    #     GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.MOTORW_A or value == GPIOPin.MOTORW_E else False)
    #     encoder = WestEncoder()
    #     encoder.move(5)
    #
    # def test_est_close(self):
    #     GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.MOTORE_B or value == GPIOPin.MOTORE_E else False)
    #     encoder = EastEncoder()
    #     encoder.steps = 10
    #     encoder.move(5)
    #
    # def test_west_close(self):
    #     GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.MOTORW_B or value == GPIOPin.MOTORW_E else False)
    #     encoder = WestEncoder()
    #     encoder.steps = 10
    #     encoder.move(5)



    # TODO improve these tests
    # def test_count_step(self):
    #     encoder = WestEncoder()
    #     GPIOConfig.status = MagicMock(side_effect=lambda value: value != GPIOPin.DT_W)
    #     encoder.target = 100
    #     encoder.__count_steps__()
    #     self.assertEqual(1, encoder.steps)
    #
    # def test_count_step_back(self):
    #     GPIOConfig.status = MagicMock(side_effect=lambda value: value == GPIOPin.DT_W)
    #     encoder = WestEncoder()
    #     encoder.steps = 5
    #     encoder.target = 1
    #     encoder.__count_steps__()
    #     self.assertEqual(4, encoder.steps)

if __name__ == '__main__':
    unittest.main()
