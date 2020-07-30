import config
from RPi import GPIO
from time import sleep
import time
from gpio_pin import GPIOPin
from gpio_config import GPIOConfig
from base.singleton import Singleton
import threading
from status import Status

GPIO.setwarnings(False)

class Encoder:
    def __init__(self):
        self.steps = 0
        self.gpioconfig = GPIOConfig()
        self.encoder_a = False
        self.encoder_b = False
        self.lockRotary = threading.Lock()
        self.dt = None
        self.clk = None


    def __event_detect__(self):
        if config.Config.getInt("count_steps_simple", "encoder_step") == 0: 
            self.gpioconfig.add_event_detect_both(self.dt, callback=self.__count_steps__)
            self.gpioconfig.add_event_detect_both(self.clk, callback=self.__count_steps__)
            print (self.dt)
            print (self.clk)        
    
    def __remove_event_detect__(self):
        self.gpioconfig.remove_event_detect(self.dt)
        self.gpioconfig.remove_event_detect(self.clk)

    def __count_steps__(self, dt_or_clk):
        self.encoder_a = self.gpioconfig.status(self.dt)
        self.encoder_b = self.gpioconfig.status(self.clk)
        if self.encoder_a and self.encoder_b:
            self.lockRotary.acquire()
            try:
                if dt_or_clk == self.clk:
                    self.steps -= 1
                elif dt_or_clk == self.dt:
                    self.steps += 1
            finally:
                self.lockRotary.release()

class WestEncoder(Encoder, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.clk_w = GPIOPin.CLK_W
        self.dt_w = GPIOPin.DT_W  
        self.__event_detect__()

class EastEncoder(Encoder, metaclass=Singleton):
    def __init__ (self):
        super().__init__()                            
        self.clk_e = GPIOPin.CLK_E
        self.dt_e = GPIOPin.DT_E
        self.__event_detect__()