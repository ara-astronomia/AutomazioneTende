import config
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
roof_verify_closed = config.Config.getValue("roof_verify_open", 'roof_board') # 11
roof_verify_open = config.Config.getValue("roof_verify_open", 'roof_board') # 7
roof_open = config.Config.getValue("roof_open", 'roof_board') # 7
roof_closed = config.Config.getValue("roof_closed", 'roof_board') # 15

GPIO.setup(roof_verify_closed, GPIO.IN, pull_up-down=GPIO.PUD_UP)
GPIO.setup(roof_verify_open, GPIO.IN, pull_up-down=GPIO.PUD_UP)
GPIO.setup(roof_open,GPIO.OUT)
GPIO.setup(roof_closed,GPIO.OUT)

def verify_closed_roof():
    GPIO.wait_for_edge(roof_verify_closed, GPIO.FALLING) # verifica che lo stato del pin sia alto, e restituisce O quando questo cambia alla pressione dell'interruttore
    status_c = 1
    sleep(config.Config.getFloat("sleep"))

def verify_open_roof():
    GPIO.wait_for_edge(roof_verify_open, GPIO.FALLING) # verifica che lo stato del pin sia alto, e restituisce O quando questo cambia alla pressione dell'interruttore
    status_o = 0
    sleep(config.Config.getFloat("sleep"))

def open_roof():
    GPIO.output(roof_open,GPIO.HIGH)
 """ da implementare le condizioni che generano gli status """   
    status_o = 1
    status_c = 0
    sleep(config.Config.getFloat("sleep"))

def closed_roof():
    GPIO.output(roof_closed,GPIO.HIGH)
 """ da implementare le condizioni che generano gli status """  
    status_o = 0
    status_c = 1
    sleep(config.Config.getFloat("sleep"))

