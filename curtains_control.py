from status import CurtainStatus
from transition_error import TransitionError
from base.singleton import Singleton
from gpio_pin import GPIOPin
from logger import Logger
from gpio_config import GPIOConfig

class CurtainControl:

    def __init__(self):
        self.gpioconfig = GPIOConfig()

    def open(self):
        self.gpioconfig.turn_on(self.pinA)
        self.gpioconfig.turn_off(self.pinB)
        self.gpioconfig.turn_on(self.pinE)
        return self.read()

    def close(self):
        self.gpioconfig.turn_off(self.pinA)
        self.gpioconfig.turn_on(self.pinB)
        self.gpioconfig.turn_on(self.pinE)
        return self.read()

    def stop(self):
        self.gpioconfig.turn_off(self.pinA)
        self.gpioconfig.turn_off(self.pinB)
        self.gpioconfig.turn_off(self.pinE)
        return self.read()

    def read(self):
        self.is_open = self.gpioconfig.status(self.pinA)
        self.is_close = self.gpioconfig.status(self.pinB)
        self.is_enable = self.gpioconfig.status(self.pinE)
        if self.is_open and self.is_enable and not self.is_close:
            return CurtainStatus.OPENING
        elif self.is_enable and self.is_close and not self.is_open:
            return CurtainStatus.CLOSING
        elif not self.is_enable:
            return CurtainStatus.STOPPED
        else:
            raise TransitionError("""Curtain state invalid - La tenda è
            in uno stato invalido""")

        # #aggiunta del controllo dello status OPEN e CLOSED delle tende tramite lettura dello stautus degli switch rispettivi
        # is_curtain_W_closed = self.gpioconfig.status(GPIOPin.CURTAINS_VERIFY_CLOSED_W) #verifica lo stato dello swicth di fine corsa in chiusura della tenda West
        # is_curtain_W_open = self.gpioconfig.status(GPIOPin.CURTAINS_VERIFY_OPEN_W) #verifica lo stato dello swicth di fine corsa in apertura della tenda West
        # is_curtain_E_closed = self.gpioconfig.status(GPIOPin.CURTAINS_VERIFY_CLOSED_E) #verifica lo stato dello swicth di fine corsa in chiusura della tenda Est
        # is_curtain_E_open = self.gpioconfig.status(GPIOPin.CURTAINS_VERIFY_OPEN_E) #verifica lo stato dello swicth di fine corsa in apertura della tenda Est


        # if is_curtain_W_closed and is_curtain_W_open:
        #     raise TransitionError("""Curtain W state invalid - La Tenda West è in uno stato invalido""")
        # if is_curtain_E_closed and is_curtain_E_open:
        #     raise TransitionError("""Curtain W state invalid - La Tenda Est è in uno stato invalido""")
        #
        # elif is_curtain_W_closed:
        #     return CurtainStatus.W_CLOSED #ritorna lo stato dello swicth di fine corsa in chiusura della tenda West
        # elif is_curtain_W_open:
        #     return CurtainStatus.W_OPEN #ritorna lo stato dello swicth di fine corsa in apertura della tenda West
        # elif is_curtain_E_closed:
        #     return CurtainStatus.E_CLOSED #ritorna lo stato dello swicth di fine corsa in chiusura della tenda Est
        # elif is_curtain_E_open:
        #     return CurtainStatus.E_OPEN #ritorna lo stato dello swicth di fine corsa in apertura della tenda Est

class EastCurtain(CurtainControl, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.pinA = GPIOPin.MOTORE_A
        self.pinB = GPIOPin.MOTORE_B
        self.pinE = GPIOPin.MOTORE_E

class WestCurtain(CurtainControl, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.pinA = GPIOPin.MOTORW_A
        self.pinB = GPIOPin.MOTORW_B
        self.pinE = GPIOPin.MOTORW_E
