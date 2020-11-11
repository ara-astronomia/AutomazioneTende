import RPi.GPIO as GPIO  # type: ignore
from logger import Logger
from base.singleton import Singleton
from gpio_pin import GPIOPin
import config


class GPIOConfig(metaclass=Singleton):

    def __init__(self):
        GPIOPin.setup()

    def turn_on(self, pin):
        GPIO.output(pin.id_pin, pin.on_is)

    def turn_off(self, pin):
        GPIO.output(pin.id_pin, not pin.on_is)

    def wait_for_on(self, switch, timeout=config.Config.getInt("wait_for_timeout", "roof_board")):
        is_finished = GPIO.wait_for_edge(switch.id_pin, GPIO.FALLING, timeout=timeout)
        return is_finished is not None

    def wait_for_off(self, switch, timeout=config.Config.getInt("wait_for_timeout", "roof_board")):
        is_finished = GPIO.wait_for_edge(switch.id_pin, GPIO.RISING, timeout=timeout)
        return is_finished is not None

    def status(self, pin):
        status = GPIO.input(pin.id_pin)
        if pin.on_is:
            if status is pin.on_is:
                return GPIO.HIGH
            else:
                return GPIO.LOW
        else:
            return status

    def add_event_detect_on(self, switch, callback, bouncetime=config.Config.getInt("event_bouncetime", "roof_board")):
        self.add_event_detect(switch, GPIO.FALLING, callback, bouncetime)

    def add_event_detect_off(self, switch, callback, bouncetime=config.Config.getInt("event_bouncetime", "roof_board")):
        self.add_event_detect(switch, GPIO.RISING, callback, bouncetime)

    def add_event_detect_both(self, switch, callback, bouncetime=config.Config.getInt("event_bouncetime", "roof_board")):
        self.add_event_detect(switch, GPIO.BOTH, callback, bouncetime)

    def add_event_detect(self, switch, edge, callback, bouncetime):
        GPIO.add_event_detect(switch.id_pin, edge, callback=callback, bouncetime=bouncetime)

    def remove_event_detect(self, switch):
        GPIO.remove_event_detect(switch.id_pin)

    def cleanup(self, n):
        GPIO.cleanup()
        exit(n)
