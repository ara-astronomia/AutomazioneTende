import unittest
from encoders_control import WestEncoder, EastEncoder
from unittest.mock import MagicMock
from gpio_config import GPIOConfig
from gpio_pin import GPIOPin
from base.singleton import Singleton
from threading import Thread
import time

def add_event_detect_both(s, pin, callback, bouncetime=0):
    add_event_detect(pin, "BOTH", callback=callback, bouncetime=bouncetime)

def add_event_detect_on(s, pin, callback, bouncetime=0):
    add_event_detect(pin, "RAISING", callback=callback, bouncetime=bouncetime)

def add_event_detect(pin, edge, callback, bouncetime):
    pin_status = GPIOConfig.status(pin)
    def thread_function(pin, pin_status, edge, callback, bouncetime):
        while True:
            new_pin_status = GPIOConfig.status(pin)
            if ((edge == "BOTH" and pin_status != new_pin_status) or
              (edge == "FALLING" and pin_status == True and new_pin_status == False) or
              (edge == "RAISING" and pin_status == False and new_pin_status == True)):
                callback(pin)
                pin_status = new_pin_status
            time.sleep(bouncetime/1000)

    thread = Thread(target=thread_function, args=(pin, pin_status, edge, callback, bouncetime))
    thread.start()

class EncoderTest(unittest.TestCase):

    def setUp(self):
        Singleton._instances = {}

    def test_est_open(self):
        GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.MOTORE_A or value == GPIOPin.MOTORE_E else False)
        encoder = EastEncoder()
        encoder.move(5)

    def test_west_open(self):
        GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.MOTORW_A or value == GPIOPin.MOTORW_E else False)
        encoder = WestEncoder()
        encoder.move(5)

    def test_est_close(self):
        GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.MOTORE_B or value == GPIOPin.MOTORE_E else False)
        encoder = EastEncoder()
        encoder.steps = 10
        encoder.move(5)

    def test_west_close(self):
        GPIOConfig.status = MagicMock(side_effect=lambda value: True if value == GPIOPin.MOTORW_B or value == GPIOPin.MOTORW_E else False)
        encoder = WestEncoder()
        encoder.steps = 10
        encoder.move(5)

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
