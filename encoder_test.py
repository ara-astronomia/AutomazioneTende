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
        self.gpiopin = GPIOPin
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
        #self.encoder_a = self.gpioconfig.status_pull(self.dt)
        #print (self.encoder_a)
        #self.encoder_b = self.gpioconfig.status_pull(self.clk)
        #print (self.encoder_b)
        print (dt_or_clk)
        print ("clk",self.clk)
        print ("dt",self.dt)
        clkLast = GPIO.input(18)
        counter = 0
        #if self.encoder_a and self.encoder_b:
        #    self.lockRotary.acquire()
        try:
            while True:
                clk = GPIO.input(18)
                dt = GPIO.input(22)
                if clk != clkLast:
                    if dt != clk:
                        counter += 1
                    else:
                        counter -= 1
                    print("counter", counter)
                    clkLast = clk
                sleep(0.001)
        finally:
            GPIO.cleanup() 
        #   self.lockRotary.release()
                        
class WestEncoder(Encoder, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.clk = self.gpiopin.CLK_W
        self.dt = self.gpiopin.DT_W
        self.__event_detect__()

class EastEncoder(Encoder, metaclass=Singleton):
    def __init__ (self):
        super().__init__()                            
        self.clk = self.gpiopin.CLK_E
        self.dt = self.gpiopin.DT_E
        self.__event_detect__()

        '''         if dt_or_clk == 18: # self.clk:
                    self.steps -= 1
                    print ("clk", self.steps)
                elif dt_or_clk == 22: # self.dt:
                    self.steps += 1
                    print ("dt", self.steps)

                print ("steps", self.steps)    
            finally:'''