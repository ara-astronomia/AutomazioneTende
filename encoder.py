import config
from RPi import GPIO
from time import sleep

clk_e = config.Config.getValue("clk_e") #17
dt_e = config.Config.getValue("dt_e") #18

clk_w = config.Config.getValue("clk_w") #22
dt_w= config.Config.getValue("dt_w") #23

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk_e, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt_e, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(clk_w, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt_w, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def encoder_est
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
                            print counter
                    clkLastState_e = clkState_e
                    sleep(0.01)

def encoder_west
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
                            print counter
                    clkLastState_w = clkState_w
                    sleep(0.01)                
                
                
                
                
finally:
GPIO.cleanup()