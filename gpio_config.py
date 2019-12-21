import RPi.GPIO as GPIO
from logger import Logger
from base.singleton import Singleton
from gpio_pin import GPIOPin

class GPIOConfig(metaclass=Singleton):

    def __init__(self):
        GPIOPin.setup()

    def turn_on(self, switch):
        GPIO.output(switch.id_pin, GPIO.HIGH)

    def turn_off(self, switch):
        GPIO.output(switch.id_pin, GPIO.LOW)

    def wait_for_raising(self, switch, timeout=60000):
        is_finished = GPIO.wait_for_edge(switch.id_pin, GPIO.RAISING, timeout=timeout)
        return is_finished != None

    def wait_for_falling(self, switch, timeout=60000):
        is_finished = GPIO.wait_for_edge(switch.id_pin, GPIO.FALLING, timeout=timeout)
        return is_finished != None

    def status(self, switch):
        return GPIO.input(switch.id_pin) == GPIO.HIGH

    def add_event_detect(self, switch, callback):
        GPIO.add_event_detect(switch.id_pin, GPIO.RISING, callback=callback)

    def remove_event_detect(self, switch):
        GPIO.remove_event_detect(switch.id_pin)
