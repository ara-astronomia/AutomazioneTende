import config
from base.singleton import Singleton
from gpio_pin import GPIOPin
from curtains_control import EastCurtain, WestCurtain
from gpio_config import GPIOConfig

class EncoderControl:
    def __init__(self):
        self.gpioconfig = GPIOConfig()
        self.target = None
        self.steps = 0
        self.__min_step__ = 0

    def __count_steps__(self):
        if self.gpioconfig.status(self.dt):
             self.steps -= 1
        else:
            self.steps += 1
        if self.steps == self.target:
            self.target = None
            self.motor.stop()
            self.gpioconfig.remove_event_detect(self.clk)
            self.moving = False

    def move(self, step):
        self.target = int(step)

        if self.steps < self.target:
            self.motor.open()
        if self.steps > self.target:
             self.motor.close()
        if self.steps != self.target:
            self.gpioconfig.add_event_detect_on(self.clk, callback=self.__count_steps__)
            self.moving = True

class WestEncoder(EncoderControl, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.__max_step__ = config.Config.getInt("n_step_finecorsa", "encoder_step")
        self.clk = GPIOPin.CLK_W
        self.dt = GPIOPin.DT_W
        self.motor = WestCurtain()

class EastEncoder(EncoderControl, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.__max_step__ = config.Config.getInt("n_step_finecorsa", "encoder_step")
        self.clk = GPIOPin.CLK_E
        self.dt = GPIOPin.DT_E
        self.motor = EastCurtain()
