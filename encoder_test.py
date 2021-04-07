import config
from RPi import GPIO
from time import sleep
import time
from gpio_pin import GPIOPin
from gpio_pin import Pin
from gpio_config import GPIOConfig
from base.singleton import Singleton
import threading
from status import Status

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


class Encoder:
    def __init__(self):
        self.steps = 0
        self.gpioconfig = GPIOConfig()
        self.gpiopin = GPIOPin
        self.pin = Pin
        self.encoder_a = False
        self.encoder_b = False
        self.lockRotary = threading.Lock()
        self.dt = None
        self.clk = None

    def __event_detect__(self):
        if config.Config.getInt("count_steps_simple", "encoder_step") == 0:
            self.gpioconfig.add_event_detect_both(self.dt, callback=self.__count_steps__)
            self.gpioconfig.add_event_detect_both(self.clk, callback=self.__count_steps__)

    def __remove_event_detect__(self):
        self.gpioconfig.remove_event_detect(self.dt)
        self.gpioconfig.remove_event_detect(self.clk)

    def __count_steps__(self, dt_or_clk):
        self.encoder_a = (self.gpioconfig.status_enc(self.dt))
        self.encoder_b = (self.gpioconfig.status_enc(self.clk))
        print("encoder_a", self.encoder_a)
        print("encoder_b", self.encoder_b)
        # GPIOPin.CLK_W = GPIO.input(18)
        # GPIOPin.DT_W = GPIO.input(22)
        # GPIOPin.CLK_E = GPIO.input(12)
        # GPIOPin.DT_E = GPIO.input(16)
        clkLast = (self.clk)
        print(clkLast)

        counter = 0
        if self.encoder_a and self.encoder_b:
            self.lockRotary.acquire()

            try:
                while True:
                    clk = self.clk
                    dt = self.dt
                    if clk != clkLast:
                        if dt != clk:
                            counter += 1
                        else:
                            counter -= 1
                        print("counter", counter)
                        clkLast = clk
                    sleep(0.01)
            finally:
                GPIO.cleanup()
                self.lockRotary.release()


class WestEncoder(Encoder, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.clk = self.gpiopin.CLK_W
        self.dt = self.gpiopin.DT_W
        self.__event_detect__()


class EastEncoder(Encoder, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.clk = self.gpiopin.CLK_E
        self.dt = self.gpiopin.DT_E
        self.__event_detect__()
