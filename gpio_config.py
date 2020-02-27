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
        return GPIO.input(switch.id_pin)

    def add_event_detect_raising(self, switch, callback, bouncetime=0):
        self.add_event_detect(switch, GPIO.RAISING, callback, bouncetime)

    def add_event_detect_falling(self, switch, callback, bouncetime=0):
        self.add_event_detect(switch, GPIO.FALLING, callback, bouncetime)

    def add_event_detect_both(self, switch, callback, bouncetime=0):
        self.add_event_detect(switch, GPIO.BOTH, callback, bouncetime)

    def add_event_detect(self, switch, edge, callback, bouncetime):
        GPIO.add_event_detect(switch.id_pin, edge, callback=callback, bouncetime=bouncetime)

    def remove_event_detect(self, switch):
        GPIO.remove_event_detect(switch.id_pin)

    def cleanup(self, n):
        GPIO.cleanup()
        exit(n)
