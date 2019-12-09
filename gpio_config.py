import RPi.GPIO as GPIO
from logger import Logger
from base.singleton import Singleton
from gpio_pin import GPIOPin

class GPIOConfig(metaclass=Singleton):

    def __init__(self):
        GPIOPin.setup()

    def turn_on(self, switch):
        GPIO.output(GPIO.input(switch), GPIO.HIGH)

    def turn_off(self, switch):
        GPIO.output(GPIO.input(switch), GPIO.LOW)

    def wait_for_raising(self, switch, timeout=60000):
        is_finished = GPIO.wait_for_edge(GPIO.input(switch), GPIO.RAISING, timeout=timeout)
        return is_finished != None

    def wait_for_falling(self, switch, timeout=60000):
        is_finished = GPIO.wait_for_edge(GPIO.input(switch), GPIO.FALLING, timeout=timeout)
        return is_finished != None

    def status(self, switch):
        return GPIO.input(switch) == GPIO.HIGH
