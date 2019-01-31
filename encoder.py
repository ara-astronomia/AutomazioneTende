import config
from RPi import GPIO
from time import sleep
from base.base_encoder import BaseEncoder

class Encoder(BaseEncoder):
    def __init__(self, orientation: "E or W"):
        self.current_step = 0
        self.__min_step__ = 0
        self.__max_step__ = int(config.Config.getValue("n_step_finecorsa"))
        # TODO set the GPIO pin based on orientation
        self.orientation = orientation
        if self.orientation == "E":
            self.clk = config.Config.getValue("clk_e") #17
            self.dt = config.Config.getValue("dt_e") #18
        elif self.orientation == "W":
            self.clk = config.Config.getValue("clk_w") #22
            self.dt = config.Config.getValue("dt_w") #23pass
        else:
            raise ValueError("devi passare E per Est e W per Ovest")

    def __save_current_step__(self, direction):

        """
            solo questo metodo andrebbe implementato diversamente nella classe che comunica con l'encoder reale:
            si dovrebbe lusare RPi.GPIO per andare a leggere l'hardware e aggiornare di conseguenza il valore degli step
        """

        self.clk_last_state = self.clk_state
        self.clk_state = GPIO.input(self.clk)
        self.dt_state = GPIO.input(self.dt)
        if direction == "F" :
            if self.clk_state != self.clk_last_state and self.dt_state == self.clk_state:
                self.__motion_step__ = self.current_step + self.clk_state
            elif self.dt_state != self.clk_state:
                raise ValueError("Motori in direzione inversa a quanto aspettato")
        elif direction == "B":
            if self.clk_state != self.clk_last_state and self.dt_state != self.clk_state:
                self.__motion_step__ = self.current_step + self.clk_state
            elif self.dt_state == self.clk_state:
                raise ValueError("Motori in direzione inversa a quanto aspettato")
        sleep(config.Config.getFloat("sleep"))

    def listen_until(self, length):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            self.clk_state = GPIO.input(self.clk)
            self.clk_last_state = self.clk_state
            self.dt_state = GPIO.input(self.dt)
            super().listen_until(length)
        finally:
            GPIO.cleanup()

def encoder_est(condition):
    counter = 0
    clkLastState_e = GPIO.input(clk_e)
    try:
        while True:
            clkState_e = GPIO.input(clk_e)
            dtState_e = GPIO.input(dt_e)
            if clkState_e != clkLastState_e:
                if dtState_e != clkState_e:
                    counter += 1
                else:
                    counter -= 1
                print(counter)
            if clkLastState_e = clkState_e or clkLastState_e = config.Config.getValue("n_step_finecorsa"):
                condition_e = 'Stop'
                sleep(config.Config.getFloat("sleep"))
    except:
        pass

def encoder_west(condition):
    counter = 0
    clkLastState_w = GPIO.input(clk_w)
    try:
        while True:
            clkState_w = GPIO.input(clk_w)
            dtState_w = GPIO.input(dt_w)
            if clkState_w != clkLastState_w:
                if dtState_w != clkState_w:
                    counter += 1
                else:
                    counter -= 1
                print(counter)
            if clkLastState_w = clkState_w or clkLastState_w = config.Config.getValue("n_step_finecorsa"):
                condition_w = 'Stop'
                sleep(config.Config.getFloat("sleep"))
    except:
        pass




#finally:
GPIO.cleanup()
