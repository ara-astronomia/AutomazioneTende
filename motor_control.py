import config
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

MotorE_A = config.Config.getValue("motorE_A") #6
MotorE_B = config.Config.getValue("motorE_B") #13
MotorE_E = config.Config.getValue("motorE_E") #5

MotorW_A = config.Config.getValue("motorW_A") #20
MotorW_B = config.Config.getValue("motorW_B") #21
MotorW_E = config.Config.getValue("motorW_E") #16

GPIO.setup(MotorE_A,GPIO.OUT)
GPIO.setup(MotorE_B,GPIO.OUT)
GPIO.setup(MotorE_E,GPIO.OUT)

GPIO.setup(MotorW_A,GPIO.OUT)
GPIO.setup(MotorW_B,GPIO.OUT)
GPIO.setup(MotorW_E,GPIO.OUT)


def go_in_open_motor_e():
    GPIO.output(MotorE_A,GPIO.HIGH)
    GPIO.output(MotorE_B,GPIO.LOW)
    GPIO.output(MotorE_E,GPIO.HIGH)
    sleep(config.Config.getFloat("sleep"))

def go_in_open_motor_w():
    GPIO.output(MotorW_A,GPIO.HIGH)
    GPIO.output(MotorW_B,GPIO.LOW)
    GPIO.output(MotorW_E,GPIO.HIGH)
    sleep(config.Config.getFloat("sleep"))

def go_in_closed_motor_e():
    GPIO.output(MotorE_A,GPIO.LOW)
    GPIO.output(MotorE_B,GPIO.HIGH)
    GPIO.output(MotorE_E,GPIO.HIGH)
    sleep(config.Config.getFloat("sleep"))

def go_in_closed_motor_w():
    GPIO.output(MotorW_A,GPIO.LOW)
    GPIO.output(MotorW_B,GPIO.HIGH)
    GPIO.output(MotorW_E,GPIO.HIGH)
    sleep(config.Config.getFloat("sleep"))

def stop_motor_e():
    GPIO.output(MotorE_E,GPIO.LOW)

def stop_motor_w():
    GPIO.output(MotorW_E,GPIO.LOW)


