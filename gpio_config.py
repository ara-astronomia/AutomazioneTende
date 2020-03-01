import RPi.GPIO as GPIO
from logger import Logger
from base.singleton import Singleton
from gpio_pin import GPIOPin
import config

class GPIOConfig(metaclass=Singleton):

    def __init__(self):
        GPIOPin.setup()

    def turn_on(self, switch):
        GPIO.output(switch.id_pin, GPIO.HIGH)

    def turn_off(self, switch):
        GPIO.output(switch.id_pin, GPIO.LOW)

    def wait_for_on(self, switch, timeout=config.Config.getInt("wait_for_timeout", "roof_board")):
        is_finished = GPIO.wait_for_edge(switch.id_pin, GPIO.FALLING, timeout=timeout)
        return is_finished != None

    def wait_for_off(self, switch, timeout=config.Config.getInt("wait_for_timeout", "roof_board")):
        is_finished = GPIO.wait_for_edge(switch.id_pin, GPIO.RAISING, timeout=timeout)
        return is_finished != None

    def status(self, switch):
        return not GPIO.input(switch.id_pin)

    def add_event_detect_on(self, switch, callback, bouncetime=config.Config.getInt("event_bouncetime", "roof_board")):
        self.add_event_detect(switch, GPIO.FALLING, callback, bouncetime)

    def add_event_detect_off(self, switch, callback, bouncetime=config.Config.getInt("event_bouncetime", "roof_board")):
        self.add_event_detect(switch, GPIO.RAISING, callback, bouncetime)

    def add_event_detect_both(self, switch, callback, bouncetime=config.Config.getInt("event_bouncetime", "roof_board")):
        self.add_event_detect(switch, GPIO.BOTH, callback, bouncetime)

    def add_event_detect(self, switch, edge, callback, bouncetime):
        GPIO.add_event_detect(switch.id_pin, edge, callback=callback, bouncetime=bouncetime)

    def remove_event_detect(self, switch):
        GPIO.remove_event_detect(switch.id_pin)

    def cleanup(self, n):
        GPIO.cleanup()
        exit(n)
