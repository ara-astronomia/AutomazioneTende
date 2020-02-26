import config
from base.singleton import Singleton
from gpio_pin import GPIOPin
from curtains_control import EastCurtain, WestCurtain
from gpio_config import GPIOConfig
import threading

class EncoderControl:
    def __init__(self):
        self.gpioconfig = GPIOConfig()
        self.target = None
        self.steps = 0
        self.__min_step__ = 0
        self.gpioconfig.add_event_detect(self.clk, callback=self.__count_steps__)
        self.gpioconfig.add_event_detect(self.dt, callback=self.__count_steps__)
        self.gpioconfig.add_event_detect(self.curtain_open, callback=self.__reset_steps__)
        self.gpioconfig.add_event_detect(self.curtain_closed, callback=self.__reset_steps__)
        self.switch_a = False
        self.switch_b = False
        self.lockRotary = threading.Lock()

    def __count_steps__(self, dt_or_clk):
        self.switch_a = self.gpioconfig.status(self.dt)
        self.switch_b = self.gpioconfig.status(self.clk)
        if self.switch_a and self.switch_b:
            self.lockRotary.acquire()
            if dt_or_clk == self.clk:
                self.steps -= 1
            else:
                self.steps += 1
            if self.steps == self.target or self.target == None:
                self.target = None
                self.motor.stop()
                self.moving = False
            self.lockRotary.release()

    def move(self, step):
        self.target = int(step)
        if self.steps < self.target:
            self.motor.open()
        if self.steps > self.target:
            self.motor.close()
        if self.steps != self.target:
            self.moving = True

    def __reset_steps__(self):
        self.lockRotary.acquire()
        self.motor.stop()
        if self.gpioconfig.status(self.curtain_open):
            self.steps = self.__max_step__
        else:
            self.steps = 0
        self.lockRotary.release()

class WestEncoder(EncoderControl, metaclass=Singleton):
    def __init__(self):
        self.__max_step__ = config.Config.getInt("n_step_finecorsa", "encoder_step")
        self.clk = GPIOPin.CLK_W
        self.dt = GPIOPin.DT_W
        self.curtain_closed = GPIOPin.CURTAIN_W_VERIFY_CLOSED
        self.curtain_open = GPIOPin.CURTAIN_W_VERIFY_OPEN
        self.motor = WestCurtain()
        super().__init__()

class EastEncoder(EncoderControl, metaclass=Singleton):
    def __init__(self):
        self.__max_step__ = config.Config.getInt("n_step_finecorsa", "encoder_step")
        self.clk = GPIOPin.CLK_E
        self.dt = GPIOPin.DT_E
        self.curtain_closed = GPIOPin.CURTAIN_E_VERIFY_CLOSED
        self.curtain_open = GPIOPin.CURTAIN_E_VERIFY_OPEN
        self.motor = EastCurtain()
        super().__init__()
