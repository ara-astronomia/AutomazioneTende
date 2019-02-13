import config
from time import sleep
import time

timeout = 5
timeout_start = time.time()


def verify_closed_roof(): #simula la condizione del fine corsa di chiusura
    status_c = 1
    return status_c
    sleep(config.Config.getFloat("sleep"))

def verify_open_roof(): # simula la condizione del fine corsa di apertura
    status_o = 0
    return status_o
    sleep(config.Config.getFloat("sleep"))

def open_roof():
    while True: 
        time.sleep(1)
        if time.time() > timeout_start + timeout:# except=RuntimeError):
            print ('Tetto Aperto')
            status_o = 1
            status_c = 0
            print (str(status_o) + " questo e' il valore di status_o ")
            return status_o
            #break        
  

def closed_roof():
  while True: 
        time.sleep(1)
        if time.time() > timeout_start + timeout:# except=RuntimeError):
            print ('Tetto Chiuso')
            status_c = 1
            status_o = 0
            print (str(status_c) + " questo e' il valore di status_o ")
            return status_c
            #break        

