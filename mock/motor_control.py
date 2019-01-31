import config
from time import sleep

def go_in_open_motor_e():
    sleep(config.Config.getFloat("sleep"))

def go_in_open_motor_w():
    sleep(config.Config.getFloat("sleep"))

def go_in_closed_motor_e():
    sleep(config.Config.getFloat("sleep"))

def go_in_closed_motor_w():
    sleep(config.Config.getFloat("sleep"))

def stop_motor_e():
    pass

def stop_motor_w():
    pass
